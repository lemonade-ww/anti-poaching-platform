import React, { Component } from 'react';
import { Table, Tag,  PageHeader } from 'antd';
import { v4 } from 'uuid';


import results from '../../json/results.json'

import './index.css'

export default class Result extends Component {
  state = {
    queryBox: {},

    columns: [
      {
        title: '#',
        dataIndex: 'num',
      },
      {
        title: '判决书标题',
        dataIndex: 'title',
        // ellipsis: true,

        render: text => <a href=':;javascript' className='list-link'>{text}</a>,
      },
      {
        title: '审理地点',
        dataIndex: 'location',

      },
      {
        title: '年份',
        dataIndex: 'year',
        defaultSortOrder: 'descend',
        sorter: (a, b) => Number(a.year) - Number(b.year),
      },
      {
        title: '被告人',
        dataIndex: 'defendant',
      },
      {
        title: '物种',
        dataIndex: 'species',
        sorter: (a, b) => a.species.length - b.species.length,
      },
      {
        title: '保护级别',
        dataIndex: 'tags',
        render: tags => (
          <>
            {tags.map(tag => {
              let color
              if (tag === '国家一级') color = 'volcano'
              else if (tag === '国家二级') color = 'green'

              return (
                <Tag color={color} key={v4()}>
                  {tag.toUpperCase()}
                </Tag>
              );
            })}
          </>
        ),
      }
    ],

    data: []
  }


  componentDidMount() {
    let arr = []

    let origin = Object.values(results)
    let num = 1

    for (let item of origin) {
      if (Object.keys(item).length !== 0) {
        let location = item.location.substring(0, item.location.length - 4)
        let year = item.number.substring(1, 5)
        let defendant = item.defendant.join('、').replace(/[ＸxX×]/g,'某')
        let species = Object.keys(item.species_info).join('、') || '不详'
        arr.push({
          num,
          title: item.title,
          location,
          year,
          defendant,
          species,
          tags: ["国家一级", "国家二级"],
          key: v4()
        })
        num++
      }
    }

    this.setState({ data: arr })
  }


  render() {
    return (
      <div className='common-container result-container'>

        <PageHeader
          className="site-page-header"
          onBack={() => window.history.back()}
          title="检索结果"
          subTitle="RESULTS"
        />

        <div className='query-box'>
          <div className='query-title'>检索条件</div>
          <p>地点：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>
          <p>时间：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>
          <p>性别：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>
          <p>年龄：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>
          <p>民族：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>
          <p>文化程度：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>
          <p>物种分类：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>
          <p>保护级别：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>
          <p>濒危等级：{this.state.queryBox.key ? this.state.queryBox.key : '不限'}</p>

          <div className='list-count'>共找到
            <span>{this.state.data.length}</span>
            条结果</div>

          <div className='result-list'>
            <Table
              columns={this.state.columns}
              pagination={{ position: ["topRight", "bottomRight"] }}
              dataSource={this.state.data}
              size='small'
            />
          </div>
        </div>


      </div>


    )

  }
}
