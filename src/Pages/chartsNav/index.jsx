import { SwapRightOutlined } from '@ant-design/icons/lib/icons'
import React, { Component } from 'react'
import { PageHeader } from 'antd';
import './index.less'

export default class ChartsNav extends Component {

  state = {
    left_img:'/img/Data_533_300.jpg',
    right_img:'/img/Data2_533_300.jpg'
  }


  render() {
    return (
      <div className='charts-nav-main common-container'>
        <PageHeader
          className="site-page-header"
          onBack={() => window.history.back()}
          title="图表"
          subTitle="CHARTS"
        />
        <div className='charts-nav-flex'>

          <div className='left' style={{backgroundImage:`url(${this.state.left_img})`}}>
            <a href='/charts/statistics'>
              <h2>数据统计</h2>
              <p>通过统计图呈现盗猎案件被告人及涉及物种的数据信息</p>
              <SwapRightOutlined className='icon'/>
            </a>
          </div>
          <div className='right' style={{backgroundImage:`url(${this.state.right_img})`}}>
            <a target='_blank' href='https://maplab.amap.com/share/mapv/e543d0c93a50c14eaebafad8ea659ade'>
                <h2>案件地图</h2>
                <p>基于案件审理地点形成的盗猎案件分布图</p>
                <SwapRightOutlined className='icon'/>
            </a>
          </div>
        
        </div>  
        
      </div>
    )
  }
}
