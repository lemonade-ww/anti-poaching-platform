import React, { Component } from 'react'
import {PageHeader} from 'antd'


import './index.less'
export default class Contact extends Component {
  render() {
    return (
      <div>
        <PageHeader
          className="site-page-header"
          onBack={() => window.history.back()}
          title="联系我们"
          subTitle="CONTACT US"
        />

        <div className='contact-content'>
          <p>研究合作：research@antipoach.com</p>
          <p>网站开发：development@antipoach.com</p>
          <p>出版合作：agency@antipoach.com</p>
          <p>影视合作：agency@antipoach.com</p>
          <p>咨询热线：400-1314-0001；010-56761988</p>
          <p>违法和不良信息举报：010-82716601 jubao@antipoach.com</p>
        </div>
      </div>
    )
  }
}
