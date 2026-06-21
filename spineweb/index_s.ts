/// <reference lib="dom"/>

import * as PIXI from 'pixi.js';
import { Spine } from 'pixi-spine';



async function initSpineCanvas() {
  // WebGL を使用するように設定を変更
  const app = new PIXI.Application({
    view: document.querySelector("canvas")!,
    width: window.innerWidth,
    height: window.innerHeight,
    backgroundAlpha: 0,
    resolution: window.devicePixelRatio || 1,
    autoDensity: true,
  });

  // Spine 3.7 用のデータを Assets でロード
  // .json, .atlas, .png が同一ディレクトリにある想定
  const skeletonData = await PIXI.Assets.load('./shinycolors/data.json');

  if (skeletonData && skeletonData.spineData) {
    const spineObj = new Spine(skeletonData.spineData);

    // スケール設定 (例: 1.0)
    spineObj.scale.set(0.7);

    // 画面中央に配置
    spineObj.x = app.screen.width / 2;
    spineObj.y = app.screen.height / 2 + 100;


    // debug
    spineObj.skeleton.data.bones.forEach((data, i) => {
      console.warn(i, "Bone ID:", data.name);
    });

    const eye = spineObj.skeleton.findBone("eye_L")

    // アニメーションの再生
    if (spineObj.state.hasAnimation('wait4')) {
      spineObj.state.setAnimation(0, 'wait4', true);
    }

    let lastclick = Date.now();

    window.addEventListener("click", () => {
      lastclick = Date.now();
      spineObj.state.setAnimation(1, 'smile2', true);
      setTimeout(() => {
        spineObj.state.clearTrack(1);
      }, 3000);
    })
    /*
        // マウス移動イベントなどで座標を更新
        window.addEventListener('pointermove', (event) => {
          // 2. ターゲットとの位置関係から角度（ラジアン）を計算
          const dx = event.clientX - window.innerWidth/2
          const dy = event.clientY - window.innerHeight/2
          const angle = Math.atan2(dy, dx);
          eye.rotation = angle
        });
    */
    setInterval(() => {
      if (lastclick < Date.now() - 20000) {
        lastclick = Date.now();
        spineObj.state.setAnimation(1, 'anger2', true);
      }
    }, 1000);

    app.stage.addChild(spineObj);
  }
}

window.addEventListener('DOMContentLoaded', initSpineCanvas);
