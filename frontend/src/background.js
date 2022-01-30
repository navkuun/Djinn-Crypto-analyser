"use strict";
import { app, protocol, BrowserWindow, ipcMain } from "electron";
import { createProtocol } from "vue-cli-plugin-electron-builder/lib";
import installExtension, { VUEJS3_DEVTOOLS } from "electron-devtools-installer";
const isDevelopment = process.env.NODE_ENV !== "production";
require("@electron/remote/main").initialize();

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { secure: true, standard: true } },
]);

async function createWindow() {
  // spawn: Running flask app as a source code(app.py)
  // When finalizing backend make flask a .exe and use execFile method
  let python = require("child_process").spawn("py", ["../backend/app.py"]);

  python.stdout.on("data", function (data) {
    console.log("data: ", data.toString("utf8"));
  });
  python.stderr.on("data", (data) => {
    console.log(`stderr: ${data}`); // when error
  });

  // Create the browser window.
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    // minWidth: 800,
    // minHeight: 600,
    show: false,
    webPreferences: {
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
      enableRemoteModule: true,
    },
  });
  let splash = new BrowserWindow({
    width: 500,
    height: 300,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
  });
  splash.loadFile("../src/splash.html");
  splash.center();

  setTimeout(function () {
    splash.close();
    win.center();
    win.show();
  }, 5000);

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL);
    if (!process.env.IS_TEST) win.webContents.openDevTools();
  } else {
    createProtocol("app");
    // Load the index.html when not in development
    win.loadURL("app://./index.html");
  }
}

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  // Killing app.exe when electron quits
  const { exec } = require("child_process");
  exec("taskkill /f /t /im app.exe", (err, stdout, stderr) => {
    if (err) {
      console.log(err);
      return;
    }

    console.log(`stdout: ${stdout}`);

    console.log(`stderr: ${stderr}`);
  });
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS);
    } catch (e) {
      console.error("Vue Devtools failed to install:", e.toString());
    }
  }
  createWindow();
});

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === "win32") {
    process.on("message", (data) => {
      if (data === "graceful-exit") {
        app.quit();
      }
    });
  } else {
    process.on("SIGTERM", () => {
      app.quit();
    });
  }
}

// to change the size of login window
ipcMain.on(
  "resize-window",
  (event, width, height, isResizable, title, isAlwaysOnTop) => {
    let browserWindow = BrowserWindow.fromWebContents(event.sender);
    browserWindow.setSize(width, height);
    // browserWindow.setMaximumSize(width, height);
    browserWindow.title = title;
    browserWindow.alwaysOnTop = isAlwaysOnTop;
  }
);
// changing size of main window
ipcMain.on(
  "resize-window-main",
  (event, width, height, isResizable, title, isAlwaysOnTop) => {
    let browserWindow = BrowserWindow.fromWebContents(event.sender);
    browserWindow.setSize(width, height, true);
    // browserWindow.setMinimumize(width, height);
    browserWindow.resizable = isResizable;
    browserWindow.title = title;
    browserWindow.alwaysOnTop = isAlwaysOnTop;
  }
);

// preventing mouseup/mousedown from going back to previous pages in app
// win.addEventListener("mouseup", (e) => {
//   if (e.button === 3 || e.button === 4) {
//     e.preventDefault();
//   }
// });
// ^ cba to work on now, will do it later so like when i'm done
