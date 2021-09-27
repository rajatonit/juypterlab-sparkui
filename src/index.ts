import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, IFrame } from '@jupyterlab/apputils';
import { PageConfig } from '@jupyterlab/coreutils';

import { Widget } from '@lumino/widgets';

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
    const { commands, shell } = app;

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
        const sparkWidget = new SparkUI();
        sparkWidget.title.label = 'Open Spark UI';

        requestAPI<any>('ui')
          .then(data => {
            console.log(data);
            const widget = new sparkUIWidget(data);
            widget.id = 'sparkui-jupyterlab';
            widget.title.label = 'SparkUI';
            widget.title.closable = true;
            shell.add(widget, 'main');
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
    const category = 'SparkUI';
    palette.addItem({
      command,
      category,
      args: { origin: 'from the palette' }
    });
  }
};

class SparkUI extends IFrame {
  // html: string;
  constructor() {
    super();
    const baseUrl = PageConfig.getBaseUrl();
    this.url = baseUrl + 'sparkuitab/';
  }
}

class sparkUIWidget extends Widget {
  /**
  * Construct a new APOD widget.
  */
  constructor(html:any) {
    super();

    this.addClass('sparkui-widget');

    // Add an image element to the panel
    this.iframe = document.createElement('iframe');
    // const baseUrl = PageConfig.getBaseUrl();
    this.iframe.setAttribute("srcdoc", html);
    this.iframe.setAttribute("width", "100%");
    this.iframe.setAttribute("height", "100%");

    this.node.appendChild(this.iframe);
  }

  /**
  * The summary text element associated with the widget.
  */
  readonly iframe: HTMLElement;

}

export default plugin;
