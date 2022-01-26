import React, { Component } from 'react';
import { Table, Tag, Space } from 'antd';
import { v4 } from 'uuid';

import { Input } from 'antd';

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

        render: text => <a href='#' className='list-link'>{text}</a>,
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

        <div className="input-group mb-3 quick-search advance-search">
          <Input placeholder="此处输入关键词，多个关键词请用空格分隔" />
          <button className="btn btn-outline-secondary"  >
            <svg viewBox="0 0 1024 1024">
              <path d="M453.818182 23.272727C704.465455 23.272727 907.636364 226.443636 907.636364 477.090909c0 35.746909-4.142545 70.981818-12.264728 105.192727a46.545455 46.545455 0 0 1-90.577454-21.504c6.469818-27.182545 9.751273-55.202909 9.751273-83.688727C814.545455 277.876364 653.032727 116.363636 453.818182 116.363636 254.603636 116.363636 93.090909 277.876364 93.090909 477.090909 93.090909 676.305455 254.603636 837.818182 453.818182 837.818182c101.003636 0 195.211636-41.658182 262.981818-113.826909a46.545455 46.545455 0 0 1 63.650909-3.979637c2.978909 1.792 5.818182 3.956364 8.401455 6.446546l213.201454 205.684363a45.707636 45.707636 0 0 1 0.581818 65.233455l-0.581818 0.581818a46.545455 46.545455 0 0 1-65.233454 0.581818l-185.390546-178.827636A452.305455 452.305455 0 0 1 453.818182 930.909091C203.170909 930.909091 0 727.738182 0 477.090909S203.170909 23.272727 453.818182 23.272727z m76.613818 179.828364c86.714182 23.598545 147.2 76.078545 177.245091 154.973091a46.545455 46.545455 0 0 1-86.993455 33.140363c-19.176727-50.362182-55.994182-82.315636-114.688-98.280727a46.545455 46.545455 0 1 1 24.436364-89.832727z" fill="#ffffff">
              </path>
            </svg>
            检索案件
          </button>
        </div>

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
