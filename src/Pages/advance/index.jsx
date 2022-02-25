import React, { Component } from 'react';
import { PageHeader, Row, Col, Alert, Button, Space } from 'antd';
import { Select, Cascader, Slider, Checkbox, Input, Card } from 'antd';
import { InfoCircleFilled } from '@ant-design/icons/lib/icons';
import { v4 } from 'uuid';
import region from '../../json/region.json'
import species from '../../json/species.json'

import './index.less'


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
      start += 3
    }
    this.setState({ options, marks_year })
  }

  render() {
    const { Option } = Select

    return (
      <div className='common-container advance-main'>

        <PageHeader
          className="site-page-header"
          onBack={() => window.history.back()}
          title="高级检索"
          subTitle="ADVANCED SEARCH"
        />

        <Alert
          showIcon
          message="后台数据完善中，检索功能暂时无法使用，欢迎点击右侧查看样例页面。"
          type="warning"
          // type="info"
          action={
            <Space>
              <Button size="small" type="link" 
                target="_blank" href="http://162.14.68.4:3000/search/result">
                查看检索结果页
              </Button>
              <Button size="small" type="link" 
                target="_blank" href="http://162.14.68.4:3000/search/case_123">
                查看判决书
              </Button>
            </Space>
          }
          closable
          style={{margin:'0 20px 10px'}}
        />

        <div className="advance-container">

          <div className='left'>
            <Card className='advanced-cards' title="案件审理属性" bordered={false}>
              <table className='advance-table'>
                <tbody>
                  <tr>
                    <td>审理地点</td>
                    <td>
                      <Cascader
                        showArrow="true"
                        style={{ width: '100%' }}
                        options={this.state.options}
                        // onChange={e => this.onChange(e)}
                        multiple
                        // maxTagCount="responsive"
                        dropdownClassName
                        placeholder="选择审理法院行政区划，可多选"
                      />
                    </td>
                  </tr>
                  <tr>
                    <td>年份</td>
                    <td >
                      <Slider className='advance-slider1'
                        range
                        max={this.state.end}
                        min={this.state.start}
                        marks={this.state.marks_year}
                        defaultValue={[2006, 2022]} />
                    </td>
                  </tr>
                </tbody>
              </table>
            </Card>

            <Card className='advanced-cards' title="被告人属性" bordered={false} style={{ marginTop: '10px' }}>
              <table className='advance-table'>
                <tbody>
                  <tr className='defendent-property-row'>
                    <td>性别</td>
                    <td>
                      <Row>
                        <Col span={8}>
                          <Checkbox defaultChecked>不限</Checkbox>
                        </Col>
                        <Col span={8}>
                          <Checkbox>男</Checkbox>
                        </Col>
                        <Col span={8}>
                          <Checkbox>女</Checkbox>
                        </Col>
                      </Row>
                    </td>
                  </tr>
                  <tr>
                    <td>年龄</td>
                    <td className='advance-slider2'>
                      <Slider range max={2000} min={1950}
                        marks={this.state.marks_age}
                        defaultValue={[1950, 2000]}
                        step={10} />
                    </td>
                  </tr>
                  <tr className='checkbox-row'>
                    <td>文化程度</td>
                    <td>
                      <Row>
                        <Col span={8}>
                          <Checkbox defaultChecked>不限</Checkbox>
                        </Col>
                        <Col span={8}>
                          <Checkbox>文盲</Checkbox>
                        </Col>
                        <Col span={8}>
                          <Checkbox>小学</Checkbox>
                        </Col>
                        <Col span={8}>
                          <Checkbox>初中</Checkbox>
                        </Col>
                        <Col span={16}>
                          <Checkbox>高中/中专/技校/职高</Checkbox>
                        </Col>
                        <Col span={8}>
                          <Checkbox>大专</Checkbox>
                        </Col>
                        <Col span={8}>
                          <Checkbox>本科</Checkbox>
                        </Col>
                        <Col span={8}>
                          <Checkbox>硕士</Checkbox>
                        </Col>
                        
                      </Row>
                    </td>
                  </tr>
                  <tr>
                    <td>民族</td>
                    <td>
                      <Select
                        mode="multiple"
                        showArrow="true"
                        allowClear
                        mode="tags" style={{ width: '100%' }} placeholder="选择民族，可多选">
                        {this.state.ethnic.map(item => (
                          <Option key={v4()}>{item}</Option>
                        ))}
                      </Select>
                    </td>
                  </tr>
                </tbody>
              </table>
            </Card>
          </div>

          <div className='right'>
            <Card className='advanced-cards' title="物种属性" bordered={false}>
              <table className='advance-table'>
                <tbody>
                  <tr>
                    <td>物种分类</td>
                    <td>
                      <Cascader
                        showArrow="true"
                        style={{ width: '100%' }}
                        options={this.state.SpeciesOptions}
                        // onChange={e => this.onChange(e)}
                        multiple
                        // maxTagCount="responsive"
                        dropdownClassName
                        placeholder='选择生物学分类（门纲目科属种），可多选'
                      />
                    </td>
                  </tr>

                  <tr className='checkbox-row'>
                    <td>保护级别</td>
                    <td>
                      <Row>
                        <Col span={24}>
                          <Checkbox defaultChecked>不限</Checkbox>
                        </Col>
                        <Col span={24}>
                          <Checkbox>国家一级保护动物</Checkbox>
                        </Col>
                        <Col span={24}>
                          <Checkbox>国家二级保护动物</Checkbox>
                        </Col>
                        <Col span={24}>
                          <Checkbox>国家 “三有” 保护动物</Checkbox>
                        </Col>
                      </Row>
                    </td>
                  </tr>

                  <tr className='checkbox-row'>
                    <td>濒危等级(IUCN)</td>
                    <td>
                      <Row>
                        <Col span={12}>
                          <Checkbox defaultChecked>不限</Checkbox>
                        </Col>
                        {
                          ['绝灭(EX)', '野外绝灭(EW)', '极危(CR)', '濒危(EN)', '易危(VU)', '近危(NT)', '无危(LC)', '数据缺乏(DD)', '未予评估(NE)'].map((value) => {
                            return (
                              <Col span={12}>
                                <Checkbox>{value}</Checkbox>
                              </Col>
                            )
                          })
                        }
                      </Row>
                    </td>
                  </tr>

                </tbody>
              </table>
            </Card>

            <Card className='advanced-cards' title="关键字" bordered={false}
              style={{ marginTop: '10px' }}>
              <table className='advance-table'>
                <tbody>
                  <tr>
                    <td>关键字</td>
                    <td>
                      <Input placeholder=""
                        style={{ hight: '28px' }}
                        allowClear={true}
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </Card>
          </div>

        </div>

        <div className='advance-bottom'>
          <div className='advance-tip'>
            <InfoCircleFilled className="info-icon" />
            提示：未填写的条件，默认为“不限”
          </div>

          <div className="quick-search advance-button">
            <button className="btn btn-outline-secondary"  >
              <svg viewBox="0 0 1024 1024"><path d="M453.818182 23.272727C704.465455 23.272727 907.636364 226.443636 907.636364 477.090909c0 35.746909-4.142545 70.981818-12.264728 105.192727a46.545455 46.545455 0 0 1-90.577454-21.504c6.469818-27.182545 9.751273-55.202909 9.751273-83.688727C814.545455 277.876364 653.032727 116.363636 453.818182 116.363636 254.603636 116.363636 93.090909 277.876364 93.090909 477.090909 93.090909 676.305455 254.603636 837.818182 453.818182 837.818182c101.003636 0 195.211636-41.658182 262.981818-113.826909a46.545455 46.545455 0 0 1 63.650909-3.979637c2.978909 1.792 5.818182 3.956364 8.401455 6.446546l213.201454 205.684363a45.707636 45.707636 0 0 1 0.581818 65.233455l-0.581818 0.581818a46.545455 46.545455 0 0 1-65.233454 0.581818l-185.390546-178.827636A452.305455 452.305455 0 0 1 453.818182 930.909091C203.170909 930.909091 0 727.738182 0 477.090909S203.170909 23.272727 453.818182 23.272727z m76.613818 179.828364c86.714182 23.598545 147.2 76.078545 177.245091 154.973091a46.545455 46.545455 0 0 1-86.993455 33.140363c-19.176727-50.362182-55.994182-82.315636-114.688-98.280727a46.545455 46.545455 0 1 1 24.436364-89.832727z" fill="#ffffff"></path></svg>
              高级检索
            </button>
          </div>
        </div>

        {/* <div style={{ float: 'right' }}>
          <a target="_blank" href="http://localhost:3000/search/case_123"> {`👉判决书-样例`}</a>
          <a target="_blank" href="http://localhost:3000/search/result"> {`👉检索结果-样例`}</a>
        </div> */}


      </div>
    )
  }
}


