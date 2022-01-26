import React from 'react'
import { v4 } from 'uuid';
import { Checkbox, Button } from 'antd';
import './index.css'


export default function Case() {
  // let { caseId } = useParams();

  const [caseInfo] = React.useState(
    {
      "defendant": [
        "张某某",
        "雷某某"
      ],
      "location": "洛南县人民法院",
      "defendant_info": [
        {
          "name": "张某某",
          "gender": "男",
          "birth": "1962年4月7日",
          "race": "汉族",
          "education_level": "小学文化",
          "is_valid_person": true,
          "all_found": true
        },
        {
          "name": "雷某某",
          "gender": "男",
          "birth": "1972年6月14日",
          "race": "汉族",
          "education_level": "初中文化",
          "is_valid_person": true,
          "all_found": true
        }
      ],
      "sentence": [
        "依据《中华人民共和国刑法》第三百四十一条第一款、第六十七条第三款、第七十二条第一款、第三款、第七十三条第二款、第三款之规定，判决如下：",
        "一、被告人张某某犯非法收购珍贵、濒危野生动物、珍贵、濒危野生动物制品罪，判处有期徒刑一年又六个月，宣告缓刑二年（缓刑考验期限，从判决确定之日起计算），并处罚金三千元。",
        "二、被告人雷某某犯非法出售珍贵、濒危野生动物罪，判处有期徒刑六个月，宣告缓刑一年（缓刑考验期限，从判决确定之日起计算），并处罚金一千元。"
      ],
      "species_info": {
        "红腹锦鸡": "鸟纲 鸡形目 雉科 锦鸡属",
        "苍鹰": "鸟纲 鹳形目 鹰科 鹰属"
      },
      "title": "被告人张某某非法收购珍贵、濒危野生动物、珍贵、濒危野生动物制品，被告人雷某某非法出售珍贵、濒危野生动物一审刑事判决书",
      "number": "（2014）洛南刑初字第00034号"
    }
  )
  let trans = (obj) => {
    let arr = []
    for (let k in obj) {
      let temp = obj[k].split(' ')
      temp.unshift(k)
      arr.push(temp)
    }
    return arr
  }

  let refineOptions = () => {
    let gender = new Set(), race = new Set(), edu = new Set(), speciesN = new Set(), classN = new Set(), orderN = new Set(), familyN = new Set(), genusN = new Set()
    caseInfo.defendant_info.forEach(item => {
      gender.add(item.gender)
      race.add(item.race)
      edu.add(item.education_level)
    })
    trans(caseInfo.species_info).forEach(item => {
      speciesN.add(item[0])
      classN.add(item[1])
      orderN.add(item[2])
      familyN.add(item[3])
      genusN.add(item[4])
    })
    const arr = [
      {
        title: '根据审理信息筛选',
        opt: [
          ['地点', [caseInfo.location.substring(0, caseInfo.location.length - 4)]],
          ['年份', [caseInfo.number.substring(1, 5)]]
        ]
      },
      {
        title: '根据被告人信息筛选',
        opt: [
          ['性别', [...gender]],
          ['民族', [...race]],
          ['教育水平', [...edu]],
        ]
      },
      {
        title: '根据物种信息筛选',
        opt: [
          ['种名', [...speciesN]],
          ['纲名', [...classN]],
          ['目名', [...orderN]],
          ['科名', [...familyN]],
          ['属名', [...genusN]],
        ]
      }
    ]
    return arr
  }


  const [options] = React.useState(refineOptions())

  return (
    <div className='common-container case-main'>

      <form className='related-search-container'>
        
        <div className="accordion" id="accordionPanelsStayOpenExample">  {/* 原始外层容器 */}
          
          {
            options.map((item,index) => (
              <div className="accordion-item border-0" key={v4()}>
                <h2 className="accordion-header" id={"heading"+index} key={v4()}>
                  <button className="accordion-button collapsed " type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target={"#collapse"+index} 
                    aria-expanded="false" 
                    aria-controls={"collapse"+index} 
                    key={v4()} >
                    {item.title}
                  </button>
                </h2>

                {/* 折叠卡内部容器 */}
                <div id={"collapse"+index} 
                  className="accordion-collapse collapse  " 
                  aria-labelledby={"heading"+index} 
                  key={v4()} >
                  <div className="accordion-body " key={v4()}>
                    {item.opt.map((v)=>(
                      <div key={v4()}>
                        <div className='check-cate' key={v4()}>{'- '+v[0]}</div>
                        {v[1].map((v2)=>(
                            <Checkbox size='sm' key={v4()} className='related-checkBox'>{v2}</Checkbox>
                        ))}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))
          }


        </div>

        <Button type="submit" type="primary" size='small' className="related-search-btn">搜索相似案件</Button>
      </form>

      <div className='case-container'>

        <table className="table align-middle">
          <thead className="table-light">
            <tr>
              <td className='case-title' colSpan='2'>{caseInfo.title}</td>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th>审理法院</th>
              <td>{caseInfo.location}</td>
            </tr>
            <tr>
              <th>案号</th>
              <td>{caseInfo.number}</td>
            </tr>
            <tr>
              <th>被告人</th>
              <td>{caseInfo.defendant.join('，')}</td>
            </tr>
            <tr>
              <th>被告人信息</th>
              <td className='p-0'>
                <table className='table mb-0'>
                  <tbody>
                    <tr>
                      <td>姓名</td>
                      <td>性别</td>
                      <td>出生日期</td>
                      <td>民族</td>
                      <td>教育水平</td>
                    </tr>
                    {caseInfo.defendant_info.map((item) => (
                      <tr key={v4()}>
                        <td>{item.name}</td>
                        <td>{item.gender}</td>
                        <td>{item.birth}</td>
                        <td>{item.race}</td>
                        <td>{item.education_level}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </td>
            </tr>
            <tr>
              <th>判决结果</th>
              <td className='pt-3 pb-2'>{caseInfo.sentence.map((item) => (<p className='lh-base pb-1' key={v4()}>{item}</p>))}</td>
            </tr>
            <tr>
              <th>案件涉及的野生动物</th>
              <td className='p-0'>
                <table className='table mb-0 '>
                  <tbody>
                    <tr>
                      <td>物种名称</td>
                      <td>纲</td>
                      <td>目</td>
                      <td>科</td>
                      <td>属</td>
                    </tr>
                    {trans(caseInfo.species_info).map((item) => (
                      <tr key={v4()}>
                        <td>{item[0]}</td>
                        <td>{item[1]}</td>
                        <td>{item[2]}</td>
                        <td>{item[3]}</td>
                        <td>{item[4]}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </td>
            </tr>
          </tbody>
        </table>

      </div>

    </div>
  )

}
