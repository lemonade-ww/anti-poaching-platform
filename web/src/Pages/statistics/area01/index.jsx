import React, { Component } from 'react'
import { Area } from '@ant-design/plots';
import data from '../../../json/area_data.json'

import './index.less'

export default class Area01 extends Component {
  render() {

    const config = {
      data,
      xField: 'date',
      yField: 'value',
      seriesField: 'country',
    };

    return (
      <div className='area-main'>
        <div className='title'>数据趋势</div>
        <Area {...config} />
      </div>
    )
  }
}
