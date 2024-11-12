import { appWindow } from '@tauri-apps/api/window';

document.getElementById('hover-icon').addEventListener('click', async () => {
  await appWindow.show();
  await appWindow.setFocus();
});
