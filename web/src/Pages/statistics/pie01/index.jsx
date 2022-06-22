import React, { Component } from 'react'
import { Pie } from '@ant-design/plots';
import moment from 'moment';

import refineFunc from './refine'
import './index.less'
import { DatePicker } from 'antd';

export default class Pie01 extends Component {

  disabledDate = (time) => {
    // Can not select days before today and today
    return time < moment().year(2006) || time > moment();
  }

  onChange = (value)=>{
    // 时间选择变化的回调
    console.log(value);
  }

  render() {
    const { RangePicker } = DatePicker;

    let config = {
      appendPadding: 10,
      data: refineFunc(this.props.keyword),
      angleField: 'value',
      colorField: 'type',
      radius: 0.75,
      label: {
        type: 'spider',
        labelHeight: 28,
        content: '{name}\n{percentage}',
      },
      interactions: [{ type: 'element-selected' }, { type: 'element-active' }],
    }

    return (
      <div className='pie-main'>
        <div className='title'>数据总计</div>
        <div className='range-cont'>
          <div className='range-title'>年份范围：</div>
          <RangePicker 
            picker="year" 
            disabledDate={this.disabledDate}
            defaultValue={[moment('2006'), moment('2022')]}
            onChange={(value)=>this.onChange(value)}
            />
        </div>
        <Pie {...config}/>
      </div>
    )
  }
}
