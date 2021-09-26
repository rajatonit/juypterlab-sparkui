import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

/**
 * Initialization data for the juypterlab-sparkui-tab extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'juypterlab-sparkui-tab:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension juypterlab-sparkui-tab is activated!');

    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The juypterlab_sparkui_tab server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
