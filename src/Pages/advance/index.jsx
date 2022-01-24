import React, { Component } from 'react';
import { Button, DatePicker, Space, Cascader, Slider, Checkbox} from 'antd';
import locale from 'antd/lib/locale/zh_CN';
import region from '../../json/region.json'

import './index.css'




export default class index extends Component {

  state = {
    options: [],
    start: 2006,
    end: 2022,
    marks_year: {},
    marks_age:{
      1950:'50后',
      1960:'60后',
      1970:'70后',
      1980:'80后',
      1990:'90后',
      2000:'00后',
    }
  }

  onChange = e => {
    console.log(e);
  };

  componentDidMount(){
    let {start,end,marks_year} = this.state
    let options = region.map(item => (
      {
        label: item.name,
        value: item.code,
        children: item.children.map(item => (
          {
            label: item.name,
            value: item.code,
            children: item.children.map(item => (
              {
                label: item.name,
                value: item.code
              }
            ))
          }
        ))
      }
    ))

    start++
    while(start <= end){
      console.log(start);
      marks_year[start] = start+''
      start += 2
    }
    this.setState({options,marks_year})
  }

  render() {
    const { RangePicker } = DatePicker;

    return (
    <div className='common-container advance-container'>
      1111
      <p>it's a p</p>


      <Cascader
      style={{ width: '100%' }}
      options={this.state.options}
      onChange={e => this.onChange(e)}
      multiple
      maxTagCount="responsive"
      />

      <Slider range  max={this.state.end} min={this.state.start}  marks={this.state.marks_year} defaultValue={[2006, 2022]} />



      <Checkbox>男</Checkbox>
      <Checkbox>女</Checkbox>

      <Slider range  max={2000} min={1950}  marks={this.state.marks_age} defaultValue={[1950, 2000]} step={10} />
    
      <Checkbox>文盲</Checkbox>
      <Checkbox>小学</Checkbox>
      <Checkbox>初中</Checkbox>
      <Checkbox>高中/中专/技校/职高</Checkbox>
      <Checkbox>大专</Checkbox>
      <Checkbox>本科</Checkbox>
      <Checkbox>硕士及以上</Checkbox>




      <Button type="primary">Button</Button>

    </div>
    )
  }
}
