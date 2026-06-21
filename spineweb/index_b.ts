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
  // .json, .atlas, .png が同一ディレクトリにある想定 hina=63 mika=69
  const skeletonData = await PIXI.Assets.load('./ch0063_home/CH0063_home.skel');

  if (skeletonData && skeletonData.spineData) {
    const spineObj = new Spine(skeletonData.spineData);

    // スケール設定 (例: 1.0)
    // 画面中央に配置

    /*
    // mika
    spineObj.scale.set(0.25);
    spineObj.x = app.screen.width / 2;
    spineObj.y = app.screen.height / 2 + 250;
    */

    // hina
    spineObj.scale.set(0.25);
    spineObj.x = app.screen.width / 2 - 100;
    spineObj.y = app.screen.height / 2 + 220;

    // アニメーションの再生
    if (spineObj.state.hasAnimation('Idle_01')) {
      spineObj.state.setAnimation(0, 'Idle_01', true);
    }

    spineObj.skeleton.data.slots.forEach((slotData, i) => {
      /* Magic Mika=i>52 ;Hina=i > 58&& 185 > i */
      if (i > 58&& 185 > i) {
        //console.warn(i,"-Slot ID:", slotData.name);
        return;
      }
      //console.warn(i,"Slot ID:", slotData.name);
      /* Magic */
      spineObj.skeleton.findSlot(slotData.name).setAttachment(null);
    });


    let lastclick = Date.now();
    /*
        window.addEventListener("click", () => {
          lastclick = Date.now();
          spineObj.state.setAnimation(0, 'Pat_01_M', true);
          setTimeout(() => spineObj.state.setAnimation(0, 'Idle_01', true), 3000);
        })
    */

    /*
        setInterval(() => {
          if (lastclick < Date.now() - 20000) {
            lastclick = Date.now();
            spineObj.state.setAnimation(0, 'anger2', true);
          }
        }, 1000)
    */
    app.stage.addChild(spineObj);
  }
}

window.addEventListener('DOMContentLoaded', initSpineCanvas);
