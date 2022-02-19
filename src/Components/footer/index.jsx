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
    sponsor:'本网站由反盗猎大数据平台团队发起，通过分析裁判文书网上的判决书，以可视化大数据的形式，呈现出中国盗猎的历史信息和最新动向。网站旨在让公众更了解我们“本土”的盗猎案件，让我们用以科普、保护和立法，在这一代终止野生动物盗猎。本网站感谢XX研究团队、中国共青团、北美小象君的大力支持！',
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
