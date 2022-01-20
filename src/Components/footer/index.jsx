import React, { Component } from 'react'
import {v4} from 'uuid'
import './index.css'


export default class Footer extends Component {

  state = {
    menu:[
      {
        title:'工具',
        content:[
          {
            text:'案件检索',
            url:'#'
          },
          {
            text:'数据统计',
            url:'#'
          },
          {
            text:'热力图',
            url:'#'
          },
        ]
      },
      {
        title:'资料',
        content:[
          {
            text:'文章列表',
            url:'#'
          },
          {
            text:'政策列表',
            url:'#'
          },
          {
            text:'法律列表',
            url:'#'
          },
        ]
      },
      {
        title:'关于我们',
        content:[
          {
            text:'网站故事',
            url:'#'
          },
          {
            text:'加入我们',
            url:'#'
          },
          {
            text:'联系我们',
            url:'#'
          },
        ]
      },
    ],
    sponsor:'本网站由反盗猎大数据平台团队发起，由心疼哥哥基金会、YYDS大学研究团队赞助开发，合作伙伴：北美小象君，共青团，自然保护区研究会，芒果TV，韩红爱心基金会火星分会。',
    logos:[
      {
        src:'/img/logo1_200_200.jpg',
        alt:'自然保护区'
      },
      {
        src:'/img/logo2_200_200.jpg',
        alt:'团中央'
      },
      {
        src:'/img/logo3_200_200.jpg',
        alt:'小象君'
      }
    ]
  }

  render() {
    const {menu, logos,sponsor} = this.state
    return (
      <div className='footer-container'>
        <div className='footer-main'>
          <div className='footer-left'>
            <div className='sponsor-text'>{sponsor}</div>
            <div className='sponsor-logo-area'>
              {logos.map(item => (
                <img key={v4()} {...item} />
              ))}
            </div>
          </div>
          <div className='footer-right'>
            {
              menu.map(item => (
                <div key={v4()}  className='menu-tab'>
                  <div className='menu-title'>{item.title}</div>
                  {item.content.map(cont => (
                    <a key={v4()} href={cont.url}>{cont.text}</a>
                  ))}
                </div>
              ))
            }
          </div>
        </div>

        <div className='copy-right'>
          <div>Copyright © 2022 中国盗猎大数据平台</div>
          <div>
            <a href="#">京ICP备100**0001号</a>
            <a href="#">
              <img src="/img/公安.png"/>
              京公网安备1***000000002202号
            </a>
          </div>
        </div>
      </div>
    )
  }
}
