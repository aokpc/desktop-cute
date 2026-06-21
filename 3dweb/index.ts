import * as THREE from 'three';
import { MMDLoader } from 'three/examples/jsm/loaders/MMDLoader.js';
import { MMDAnimationHelper } from 'three/examples/jsm/animation/MMDAnimationHelper.js';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js';
import { screenToWorldPlane, worldToScreenPosition, SaturationShader, mikaInfluKey, mikaBoneKeyToIndex, globalExport } from "./helper"

let mika: THREE.SkinnedMesh<THREE.BufferGeometry<THREE.NormalBufferAttributes>, THREE.Material | THREE.Material[]>, head: THREE.Bone, neck: THREE.Bone;

const setInflu = (name: mikaInfluKey, value = 1.0) => (mika.morphTargetInfluences![mika.morphTargetDictionary![name]] = value);

const getBone = (name: (keyof typeof mikaBoneKeyToIndex)) => mika.skeleton.bones[mikaBoneKeyToIndex[name]];

const zCamera = 30;

const PATH = "/mika/聖園ミカ_ver1.11.pmx"

const canvas = document.querySelector("canvas")!;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2000);
camera.position.set(0, 15, zCamera);

const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setClearColor(0x000000, 0);
// カラーマネジメントの設定（これが無いと白っぽくなります）
renderer.outputColorSpace = THREE.SRGBColorSpace;

//const ambientLight = new THREE.AmbientLight(0xffffff, 0.2); // 強度を下げて調整
//scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.9); // 強度を下げて調整
directionalLight.position.set(0, 5, 5).normalize();
scene.add(directionalLight);

// Ammo.js の初期化
declare var Ammo: any;

async function init() {
    // 1. Ammoの初期化とグローバル化
    //const ammo = await Ammo();
    //(window as any).Ammo = ammo;

    const helper = new MMDAnimationHelper();
    const loader = new MMDLoader();

    // ポストプロセッシングの設定
    const composer = new EffectComposer(renderer);
    const renderPass = new RenderPass(scene, camera);
    composer.addPass(renderPass);

    const saturationPass = new ShaderPass(SaturationShader);
    saturationPass.uniforms['saturation'].value = 1.6; // ここで彩度を調整
    composer.addPass(saturationPass);

    loader.load(
        PATH,
        (mesh) => {
            mika = mesh;
            neck = getBone("首");
            head = getBone("頭");
            globalExport(getBone, "getBone");
            globalExport(setInflu, "setInflu");
            /*
            getBone("左肩").rotateZ(Math.PI/8);
            getBone("右肩").rotateZ(-Math.PI/8);
            */
            scene.add(mesh);

            // 2. 物理演算をして追加
            helper.add(mesh, {
                physics: false
            });

            setInflu("視線を注ぐ");
            setInflu("ヘイロー回転");

            mesh.position.set(0, 0, 0);
        },
        (xhr) => { console.warn((xhr.loaded / xhr.total * 100) + '% loaded'); },
        (error) => { console.error(error); }
    );

    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        helper.update(clock.getDelta());
        composer.render();
    }

    animate();

    let movingmika0pos: THREE.Vector3, movingpt0pos: THREE.Vector3, ispointerdown: boolean;

    onpointerdown = (e) => {
        if (mika) {
            setInflu("視線を注ぐ", 0);
            setInflu("はぅ");
            setInflu("ワ5");
            ispointerdown = true;
            movingmika0pos = mika.position.clone();
            movingpt0pos = screenToWorldPlane(e.screenX, e.screenY, camera);
        }
    }
    onpointerup = onpointercancel = () => {
        setInflu("視線を注ぐ");
        setInflu("はぅ", 0);
        setInflu("ワ5", 0);
        ispointerdown = false;
    }

    let mikapos = { x: 0, y: 0 };
    onpointermove = (e) => {
        if (head) {
            if (ispointerdown) {
                mika.position.copy(movingmika0pos.clone().add(screenToWorldPlane(e.screenX, e.screenY, camera).clone().sub(movingpt0pos)));
                mikapos = worldToScreenPosition(head, camera, renderer);
                (window as any).pyBridge && (window as any).pyBridge.postMessage(JSON.stringify(worldToScreenPosition(head, camera, renderer)));
                return mika.lookAt(0, mika.position.y, zCamera);
            }

            const mouse = screenToWorldPlane(e.screenX, e.screenY, camera, -15);
            mika.lookAt(mouse.x, mika.position.y, 25);
            head.lookAt(mouse);
        };
    };
    onmacmove = (X, Y) => {
        if (head) {
            // マウス位置を正規化デバイス座標 (-1から+1) に変換
            const mouse = screenToWorldPlane(X, Y, camera, -15);
            mika.lookAt(mouse.x, mika.position.y, 25);
            head.lookAt(mouse);
        };
    };



    const mabataki = {
        mode: 0,
        param: 0,
        interval(dt: number) {
            if (mika && (!ispointerdown)) {
                if (this.mode == 0) {
                    this.mode = 1
                    this.param = Number(document.timeline.currentTime);
                    requestAnimationFrame(this.interval.bind(this));
                } else if ((dt - this.param) >= 250) {
                    this.mode = 0
                    setInflu("まばたき", 0);
                    setTimeout(this.interval.bind(this), 5000 + Math.random() * 5000);
                } else {
                    setInflu("まばたき", 1 - 0.000064 * ((dt - 125 - this.param) ** 2));
                    requestAnimationFrame(this.interval.bind(this));
                }
            } else {
                setTimeout(this.interval.bind(this), 1000);
            }
        }
    };
    mabataki.interval(0);

    const wing = {
        interval(dt: number) {
            if (mika && (!ispointerdown)) {
                const wingL = getBone("Wing_L_0"), wingR = getBone("Wing_R_0"), sin = 1 / 16 + Math.sin(dt / 1000) / 16;
                wingL.rotation.set(sin, sin, 0);
                wingR.rotation.set(sin, -sin, 0);
            } else {
            }
            requestAnimationFrame(this.interval.bind(this));
        }
    };
    wing.interval(0);

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    setInterval(() => {
        (window as any).pyBridge && (window as any).pyBridge.postMessage(JSON.stringify(worldToScreenPosition(head, camera, renderer)));
    }, 1000);
}

init();