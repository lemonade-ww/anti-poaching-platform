import React, { Component } from 'react'
import {PageHeader} from 'antd'


import './index.less'
export default class Aboutus extends Component {
  render() {
    return (
      <div>
        <PageHeader
          className="site-page-header"
          onBack={() => window.history.back()}
          title="网站故事"
          subTitle="ABOUT US"
        />

        <div className='about-content'>
          <p>
          中国野生动物盗猎大数据平台，国内首个野生动物违法盗猎执法与判决信息聚合网站，于 2021 年 9 月 立项，2022 年 2 月正式上线，以「让人们了解中国盗猎现状，用以科普、保护和立法，在这一代终止盗猎」为使命。
          </p>
          <p>网站特点：</p>
          <ul>
            <li>所有数据都能够以可视化方式（大数据）呈现，并且查看方便</li>
            <li>数据可被过滤搜索，搜索机制简单无bug</li>
            <li>整合中国野生动物保护所有相关的法律政策</li>
            <li>录入了基本全面的中国本土野生动物案件信息</li>
            <li>定时更新数据</li>
          </ul>
        </div>
      </div>
    )
  }
}
