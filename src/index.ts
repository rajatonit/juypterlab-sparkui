import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';
import { requestAPI } from './handler';

/**
 * Initialization data for the juypterlab-sparkui-tab extension.
 */

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'juypterlab-sparkui-tab:plugin',
  autoStart: true,
  requires: [ICommandPalette],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette) => {
    console.log('JupyterLab extension juypterlab-sparkui-tab is activated!');
    const { commands } = app;

    // Add a command
    const command = 'spark:open-spark-ui';
    commands.addCommand(command, {
      label: 'Open SparkUI',
      caption:
        'Open SparkUI running for your current spark context in your notebook',
      execute: (args: any) => {
        console.log(
          `jlab-examples:main-menu has been called ${args['origin']}.`
        );

        requestAPI<any>('ui')
          .then(data => {
            console.log(data);
          })
          .catch(reason => {
            console.error(
              `The juypterlab_sparkui_tab server extension appears to be missing.\n${reason}`
            );
          });
        window.alert(
          `jlab-examples:main-menu has been called ${args['origin']}.`
        );
      }
    });

    // Add the command to the command palette
    const category = 'Spark';
    palette.addItem({
      command,
      category,
      args: { origin: 'from the palette' }
    });
  }
};

// const plugin: JupyterFrontEndPlugin<void> = {
//   id: 'juypterlab-sparkui-tab:plugin',
//   autoStart: true,
//   activate: (app: JupyterFrontEnd) => {
//     console.log('JupyterLab extension juypterlab-sparkui-tab is activated!');

//     requestAPI<any>('ui')
//       .then(data => {
//         console.log(data);
//       })
//       .catch(reason => {
//         console.error(
//           `The juypterlab_sparkui_tab server extension appears to be missing.\n${reason}`
//         );
//       });
//   }
// };

export default plugin;
