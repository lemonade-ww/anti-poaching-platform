import React, { Component } from 'react'
import MyLink from './myLink'
import './index.css'

export default class Header extends Component {
  render() {
    return (
      <div className='header-main'>

        <div className='header-logo'>
          <a href="#">
            <img src="" alt="logo" />
            <div>中国野生动物大数据平台</div>
            <div>antipoach.cn</div>
          </a>
        </div>

        <div className='header-login'>
          <a href="#">联系我们</a>
          <a href="#">注册</a>
          <a href="#">登陆</a>
        </div>

        <nav className='header-nav'>
          <MyLink to='/' name='主页'/>
          <MyLink to='/charts' name='数据统计'/>
          <MyLink to='/search' name='高级检索'/>
          <MyLink to='/about' name='关于'/>

        </nav>
        <div className='header-search'></div>
      </div>
    )
  }
}
