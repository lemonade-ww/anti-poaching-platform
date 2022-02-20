import { SwapRightOutlined } from '@ant-design/icons/lib/icons'
import React, { Component } from 'react'
import { PageHeader } from 'antd';
import './index.less'

export default class ChartsNav extends Component {

  state = {
    left_img:'/img/Data_800_450.jpg',
    right_img:'/img/Data2_800_450.jpg'
  }


  render() {
    return (
      <div className='charts-nav-main'>
        <PageHeader
          className="site-page-header"
          onBack={() => window.history.back()}
          title="图表"
          subTitle="CHARTS"
        />
        <div className='charts-nav-flex'>

          <div className='left' style={{backgroundImage:`url(${this.state.left_img})`}}>
            <a>
              <h2>数据统计</h2>
              <p>通过统计图呈现盗猎案件被告人及涉及物种的数据信息</p>
              <SwapRightOutlined className='icon'/>
            </a>
          </div>
          <div className='right' style={{backgroundImage:`url(${this.state.right_img})`}}>
            <a>
                <h2>热力图</h2>
                <p>基于案件审理地点形成的盗猎案件热力图</p>
                <SwapRightOutlined className='icon'/>
            </a>
          </div>
        
        </div>  
        
      </div>
    )
  }
}
