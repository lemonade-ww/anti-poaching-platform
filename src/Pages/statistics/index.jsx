import React, { Component } from 'react'
import { Menu } from 'antd';
import { AimOutlined, GlobalOutlined, SolutionOutlined } from '@ant-design/icons';
import Pie01 from './pie01'
import './index.less'


export default class Statistics extends Component {

  state = {
    keyword : ''
  }
  handleClick = (k)=>{
    console.log(k.key);
    console.log(this.state.keyword);
    this.setState({keyword: k.key})
  }

  render() {
    const { SubMenu } = Menu;
    return (

      <div className='statistics-main common-container'>
        <Menu
          onClick={(selectedKeys)=>this.handleClick(selectedKeys)}
          style={{ width: 256 }}
          // defaultSelectedKeys={['1']}
          defaultOpenKeys={['sub1']}
          mode="inline"
          className='left'
        >
          <SubMenu key="sub1" icon={<SolutionOutlined />} title="被告人">
            <Menu.Item key="gender">性别</Menu.Item>
            <Menu.Item key="race">民族</Menu.Item>
            <Menu.Item key="3">教育水平</Menu.Item>
            <Menu.Item key="4">盗猎目的</Menu.Item>
          </SubMenu>
          <SubMenu key="sub2" icon={<GlobalOutlined />} title="物种">
            <Menu.Item key="5">门</Menu.Item>
            <Menu.Item key="6">纲</Menu.Item>
            <Menu.Item key="7">目</Menu.Item>
            <Menu.Item key="8">科</Menu.Item>
            <Menu.Item key="9">属</Menu.Item>
            <Menu.Item key="10">种</Menu.Item>
            <Menu.Item key="11">自定义组合</Menu.Item>
          </SubMenu>
          <SubMenu key="sub3" icon={<AimOutlined />} title="判决结果">
            <Menu.Item key="12">刑罚类型</Menu.Item>
            <Menu.Item key="13">罚金</Menu.Item>
            <Menu.Item key="14">获刑时长</Menu.Item>
          </SubMenu>
        </Menu>

        <div className='right'>
          <div>
            <Pie01 keyword={this.state.keyword}></Pie01>
          </div>
          <div>

          </div>
        </div>
      </div>

    )
  }
}
