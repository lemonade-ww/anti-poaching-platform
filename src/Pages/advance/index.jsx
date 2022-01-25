import React, { Component } from 'react';
import { Button, DatePicker, Space, Cascader, Slider, Checkbox} from 'antd';
import locale from 'antd/lib/locale/zh_CN';
import region from '../../json/region.json'
import species from '../../json/species.json'

import './index.css'




export default class index extends Component {

  state = {
    options: [],
    SpeciesOptions: species,
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
      
      <div className='table-title'>案件审理属性</div>
      <table className='advance-table'>
        <tr>
          <td>审理地点</td>
          <td>
          <Cascader
            style={{ width: '100%' }}
            options={this.state.options}
            onChange={e => this.onChange(e)}
            multiple
            maxTagCount="responsive"
            dropdownClassName
            placeholder="选择审理法院所在行政单位（省级、市级、区/县级），可多选"
            />
          </td>
        </tr>
        <tr>
          <td>审理时间</td>
          <td>
            <Slider range  max={this.state.end} min={this.state.start}  marks={this.state.marks_year} defaultValue={[2006, 2022]} />
          </td>
        </tr>
      </table>

      <div className='table-title'>被告人属性</div>
      <table className='advance-table'>
        <tr>
          <td>性别</td>
          <td>
            <Checkbox>男</Checkbox>
            <Checkbox>女</Checkbox>
          </td>
        </tr>
        <tr>
          <td>年龄</td>
          <td>
            <Slider range  max={2000} min={1950}  
              marks={this.state.marks_age} 
              defaultValue={[1950, 2000]} 
              step={10} />
          </td>
        </tr>
        <tr>
          <td>文化程度</td>
          <td>
            <Checkbox>文盲</Checkbox>
            <Checkbox>小学</Checkbox>
            <Checkbox>初中</Checkbox>
            <Checkbox>高中/中专/技校/职高</Checkbox>
            <Checkbox>大专</Checkbox>
            <Checkbox>本科</Checkbox>
            <Checkbox>硕士及以上</Checkbox>
          </td>
        </tr>
      </table>

      <div className='table-title'>物种属性</div>
      <table className='advance-table'>
        <tr>
          <td>物种分类</td>
          <td>
            <Cascader
            style={{ width: '100%' }}
            options={this.state.SpeciesOptions}
            onChange={e => this.onChange(e)}
            multiple
            maxTagCount="responsive"
            dropdownClassName
            placeholder='选择案件所涉物种的生物学分类（门、纲、目、科、属、种），可多选'
            />
          </td>
        </tr>
        <tr>
          <td>保护级别</td>
          <td>
            <Checkbox>国家一级保护动物</Checkbox>
            <Checkbox>国家二级保护动物</Checkbox>
            <Checkbox>国家“三有”保护动物</Checkbox>
          </td>
        </tr>
        <tr>
          <td>IUCN濒危等级</td>
          <td>
            <Checkbox>绝灭(EX)</Checkbox>
            <Checkbox>野外绝灭(EW)</Checkbox>
            <Checkbox>极危(CR)</Checkbox>
            <Checkbox>濒危(EN)</Checkbox>
            <Checkbox>易危(VU)</Checkbox>
            <Checkbox>近危(NT)</Checkbox>
            <Checkbox>无危(LC)</Checkbox>
            <br />
            <Checkbox>数据缺乏(DD)</Checkbox>
            <Checkbox>未予评估(NE)</Checkbox>
          </td>
        </tr>
      </table>

      <div className='submit-box'>
        <div>提示：未勾选任何选项的筛选条件默认为全选</div>
        <Button type="primary" size='large' className='submit-btn'>检索案件</Button>
      </div>

    </div>
    )
  }
}
