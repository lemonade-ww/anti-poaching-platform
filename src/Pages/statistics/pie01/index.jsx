import React, { Component } from 'react'
import { Pie } from '@antv/g2plot';

import refineFunc from './refine'


export default class Pie01 extends Component {

  state = {
    keyword: this.props.keyword
  }

  renderChart = () => {
    const data = refineFunc(this.state.keyword)
    console.log(data);
    const piePlot = new Pie('container', {
      appendPadding: 10,
      data,
      angleField: 'value',
      colorField: 'type',
      radius: 0.75,
      label: {
        type: 'spider',
        labelHeight: 28,
        content: '{name}\n{percentage}',
      },
      interactions: [{ type: 'element-selected' }, { type: 'element-active' }],
    });

    piePlot.render();

  }

  componentDidMount() {
    this.renderChart()
  }

  render() {
    return (
      <div id="container"></div>
    )
  }
}
