/// <reference lib="dom"/>

import { Application, Ticker, DisplayObject } from "pixi.js";
import { Live2DModel } from "pixi-live2d-display-lipsyncpatch/cubism4";

const setModelPosition = (
  app: Application,
  model: InstanceType<typeof Live2DModel>
) => {
  const scale = (app.renderer.height * 1) / model.height;
  model.scale.set(scale);
  model.x = app.renderer.width - model.width * scale - 20;
  model.y = app.renderer.height - model.height * scale;
};

async function setupLive2D(canvas: HTMLCanvasElement) {
  const app = new Application({
    view: canvas,
    width: canvas.clientWidth,
    height: canvas.clientHeight,
    backgroundAlpha: 0,
    antialias: true,
  });

  try {
    const model = await Live2DModel.from(
      `./image_native/live2d_v4/${TARGET}/model.model3.json`,
      { ticker: Ticker.shared }
    );

    app.stage.addChild(model as unknown as DisplayObject);
    model.anchor.set(0.5, 0.5);
    setModelPosition(app, model);

    model.on("hit", (hitAreas: string[]) => {
      if (hitAreas.includes("Body")) {
        model.motion("Tap@Body");
      }
    });

    const onResize = () => {
      app.renderer.resize(canvas.clientWidth, canvas.clientHeight);
      setModelPosition(app, model);
    };

    (window as any).$move = (x: number, y: number) => model.focus(x, y);

    window.addEventListener("resize", onResize);

    // リソース解放用の関数を返す
    return {
      app,
      model,
      destroy: () => {
        window.removeEventListener("resize", onResize);
        app.destroy(true, { children: true, texture: true, baseTexture: true });
      },
    };
  } catch (error) {
    console.error("Failed to load Live2D model:", error);
    throw error;
  }
}
setupLive2D(document.querySelector("canvas")!);