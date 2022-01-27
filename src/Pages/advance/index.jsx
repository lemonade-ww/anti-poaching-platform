import React, { Component } from 'react';
import { Select, Cascader, Slider, Checkbox, Input } from 'antd';
import { InfoCircleFilled } from '@ant-design/icons/lib/icons';
import { v4 } from 'uuid';
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
    marks_age: { 1950: '50后', 1960: '60后', 1970: '70后', 1980: '80后', 1990: '90后', 2000: '00后' },
    ethnic: ["汉族", "蒙古族", "回族", "藏族", "维吾尔族", "苗族", "彝族", "壮族", "布依族", "朝鲜族", "满族", "侗族", "瑶族", "白族", "土家族", "哈尼族", "哈萨克族", "傣族", "黎族", "僳僳族", "佤族", "畲族", "高山族", "拉祜族", "水族", "东乡族", "纳西族", "景颇族", "柯尔克孜族", "土族", "达斡尔族", "仫佬族", "羌族", "布朗族", "撒拉族", "毛南族", "仡佬族", "锡伯族", "阿昌族", "普米族", "塔吉克族", "怒族", "乌孜别克族", "俄罗斯族", "鄂温克族", "德昂族", "保安族", "裕固族", "京族", "塔塔尔族", "独龙族", "鄂伦春族", "赫哲族", "门巴族", "珞巴族", "基诺族"]
  }

  componentDidMount() {
    let { start, end, marks_year } = this.state
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
    while (start <= end) {
      marks_year[start] = start + ''
      start += 2
    }
    this.setState({ options, marks_year })
  }

  render() {
    const { Option } = Select

    return (
      <div className='common-container advance-container'>

        <div className="input-group mb-3 quick-search advance-search">
          <Input placeholder="此处输入关键词，多个关键词请用空格分隔" />
          <button className="btn btn-outline-secondary"  >
            <svg viewBox="0 0 1024 1024">
              <path d="M453.818182 23.272727C704.465455 23.272727 907.636364 226.443636 907.636364 477.090909c0 35.746909-4.142545 70.981818-12.264728 105.192727a46.545455 46.545455 0 0 1-90.577454-21.504c6.469818-27.182545 9.751273-55.202909 9.751273-83.688727C814.545455 277.876364 653.032727 116.363636 453.818182 116.363636 254.603636 116.363636 93.090909 277.876364 93.090909 477.090909 93.090909 676.305455 254.603636 837.818182 453.818182 837.818182c101.003636 0 195.211636-41.658182 262.981818-113.826909a46.545455 46.545455 0 0 1 63.650909-3.979637c2.978909 1.792 5.818182 3.956364 8.401455 6.446546l213.201454 205.684363a45.707636 45.707636 0 0 1 0.581818 65.233455l-0.581818 0.581818a46.545455 46.545455 0 0 1-65.233454 0.581818l-185.390546-178.827636A452.305455 452.305455 0 0 1 453.818182 930.909091C203.170909 930.909091 0 727.738182 0 477.090909S203.170909 23.272727 453.818182 23.272727z m76.613818 179.828364c86.714182 23.598545 147.2 76.078545 177.245091 154.973091a46.545455 46.545455 0 0 1-86.993455 33.140363c-19.176727-50.362182-55.994182-82.315636-114.688-98.280727a46.545455 46.545455 0 1 1 24.436364-89.832727z" fill="#ffffff">
              </path>
            </svg>
            检索案件
          </button>
        </div>

        <div className='advance-tip'>
          <InfoCircleFilled className="info-icon" />
          勾选提示：若某一项未进行勾选，则该项默认为全选

          <a href="http://localhost:3000/search/result"> {`👉👉👉搜索结果样例页`}</a>
          <a href="http://localhost:3000/search/case_123"> {`👉👉👉判决书样例页`}</a>
        </div>

        <div className='table-title'>案件审理属性</div>
        <table className='advance-table table1'>
          <tbody>
            <tr>
              <td>审理地点</td>
              <td>
                <Cascader
                  style={{ width: '100%' }}
                  options={this.state.options}
                  onChange={e => this.onChange(e)}
                  multiple
                  // maxTagCount="responsive"
                  dropdownClassName
                  placeholder="点击选择审理法院所在行政单位（省级、市级、区/县级），可多选"
                />
              </td>
            </tr>
            <tr>
              <td>
                年份
                (范围)
              </td>
              <td >
                <Slider className='advance-slider1' range max={this.state.end} min={this.state.start} marks={this.state.marks_year} defaultValue={[2006, 2022]} />
              </td>
            </tr>
          </tbody>
        </table>

        <div className='table-title'>被告人属性</div>
        <table className='advance-table'>
          <tbody>

            <tr className='defendent-property-row'>
              <td>性别</td>
              <td>
                <Checkbox>男</Checkbox>
                <Checkbox>女</Checkbox>
              </td>
              <td>年龄(范围)</td>
              <td className='advance-slider2'>
                <Slider range max={2000} min={1950}
                  marks={this.state.marks_age}
                  defaultValue={[1950, 2000]}
                  step={10} />
              </td>
            </tr>
            <tr>
            </tr>

            <tr>
              <td>民族</td>
              <td colSpan="3">
                <Select
                  mode="multiple"
                  allowClear
                  mode="tags" style={{ width: '100%' }} placeholder="点击选择民族，可多选">
                  {this.state.ethnic.map(item => (
                    <Option key={v4()}>{item}</Option>
                  ))}
                </Select>
              </td>
            </tr>
            <tr className='checkbox-row'>
              <td>文化程度</td>
              <td colSpan="3">
                <Checkbox>文盲</Checkbox>
                <Checkbox>小学</Checkbox>
                <Checkbox>初中</Checkbox>
                <Checkbox>高中/中专/技校/职高</Checkbox>
                <Checkbox>大专</Checkbox>
                <Checkbox>本科</Checkbox>
                <Checkbox>硕士及以上</Checkbox>
              </td>
            </tr>
          </tbody>

        </table>

        <div className='table-title'>物种属性</div>
        <table className='advance-table table2'>
          <tbody>

            <tr>
              <td>物种分类</td>
              <td>
                <Cascader
                  style={{ width: '100%' }}
                  options={this.state.SpeciesOptions}
                  onChange={e => this.onChange(e)}
                  multiple
                  // maxTagCount="responsive"
                  dropdownClassName
                  placeholder='点击选择案件所涉物种的生物学分类（门、纲、目、科、属、种），可多选'
                />
              </td>
            </tr>
            <tr className='checkbox-row'>
              <td>保护级别</td>
              <td>
                <Checkbox>国家一级保护动物</Checkbox>
                <Checkbox>国家二级保护动物</Checkbox>
                <Checkbox>国家“三有”保护动物</Checkbox>
              </td>
            </tr>
            <tr className='checkbox-row'>
              <td>濒危等级(IUCN)</td>
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
          </tbody>

        </table>

      </div>
    )
  }
}


