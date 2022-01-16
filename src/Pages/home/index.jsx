import React, { Component } from 'react'
import MyTab from './myTab'
import './index.css'

export default class Home extends Component {

  state = {
    centerTitle: '面向公众的野生动物盗猎案件统计网站',
    carouselFirstUrl: '/img/2_1056_600.jpg',
    carouselFirstCaption: '中国现行的《野生动物保护法》于1989年3月开始正式施行。',
    carouselList: [
      {
        id: 2,
        url:'/img/1_1056_600.jpg',
        caption: '非法猎捕、杀害、收购、运输、出售国家重点保护濒危野生动物的，将处五年以下至十年以上有期徒刑。'
      },
      {
        id: 3,
        url:'/img/3_1056_600.jpg',
        caption: '保护濒危动物不能只保护“生物塔尖”，生物链上的塔身和塔基也应一同保护。'
      },
      {
        id: 4,
        url:'/img/4_1056_600.jpg',
        caption: '在禁猎区、禁猎期进行狩猎，破坏野生动物资源，将处三年以下有期徒刑、拘役、管制或者罚金。'
      },
      {
        id: 5,
        url:'/img/5_1056_600.jpg',
        caption: '绿水青山，就是金山银山。'
      },
    ],
    tab:{
      tab1:{
        title:'工具',
        description:'为您提供查询违法盗猎案件记录的工具，欢迎开始探索！',
        rows:{
          rows1:{
            title:'探索工具',
            mytab:[
              {
                iClass:'bi bi-search',
                aLink:'#',
                aText:'案件检索',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容',
              },
              {
                iClass:'bi bi-map-fill',
                aLink:'#',
                aText:'热力图',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容',
              },
              {
                iClass:'bi bi-bar-chart-line-fill',
                aLink:'#',
                aText:'数据统计',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容',
              }
            ]
          }
        }

      },
      tab2:{
        title:'政策与法律',
        description:'我是这个tab的说明文字，为您提供查询违法盗猎案件记录的工具，欢迎开始探索！',
        rows:{
          rows1:{
            title:'法律文件',
            mytab:[
              {
                iClass:'bi bi-book-half',
                aLink:'#',
                aText:'《野生动物保护法》',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容',
              },
              {
                iClass:'bi bi-book-half',
                aLink:'#',
                aText:'《自然保护区条例》',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容',
              }
            ]
          },
          rows2:{
            title:'政策文件',
            mytab:[]
          }
        }

      },
      tab3:{
        title:'社会机构与组织',
        description:'我是这个tab的说明文字，为您提供查询违法盗猎案件记录的工具，欢迎开始探索！',
        rows:{
          rows1:{
            title:'研究机构',
            mytab:[
              {
                iClass:'bi bi-bank2',
                aLink:'#',
                aText:'中山大学XX研究团队',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内描述内容描述内容',
              },
              {
                iClass:'bi bi-bank2',
                aLink:'#',
                aText:'昆山杜克大学XX研究团队',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容',
              }
            ]
          },
          rows2:{
            title:'公益组织',
            mytab:[
              {
                iClass:'bi bi-tree-fill',
                aLink:'#',
                aText:'小象君',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容',
              },
              {
                iClass:'bi bi-tree-fill',
                aLink:'#',
                aText:'城市荒野',
                pText:'描述内容描述内容描述内容描述内容描述内容描述内容',
              }
            ]
          }
        }
      }
    }
  }


  render() {

    const {centerTitle, 
      carouselFirstUrl,
      carouselFirstCaption,
      carouselList,
      tab} = this.state

    return (
      <div className='home-main'>

          {/* 轮播图组件容器 */}
          <div id="home-carousel" className="carousel-container carousel slide" data-bs-ride="carousel">
            {/* 轮播图切换按钮 */}
            <div className="carousel-indicators">
              <button type="button" data-bs-target="#home-carousel" data-bs-slide-to="0" className="active" aria-current="true" aria-label="Slide 1"></button>
              { carouselList.map((item)=>(
                  <button type="button" data-bs-target="#home-carousel" data-bs-slide-to={item.id-1} aria-label={`Slide ${item.id}`}></button>
                ))
              }
            </div>
            
            {/* 中心文字和搜索区 */}
            <div className='home-title-container'>
              <div className='home-title-big'>{centerTitle}</div>
              <div className='home-title-link-container'>
                <a href='#'>
                  <i className="bi bi-vector-pen"></i>
                  <p>600,000起</p>
                  <p>违法盗猎案件记录</p>
                </a>
                <a href='#'>
                  <i className="bi bi-server"></i>
                  <p>980种8类</p>
                  <p>国家重点保护动物</p>
                </a>
              </div>
              <form className="input-group mb-3 home-title-search">
                <input type="text" class="form-control" placeholder="输入物种名或地区，查询野生动物盗猎案件" aria-label="Recipient's username" aria-describedby="button-addon2"/>
                <button class="btn btn-outline-secondary" type="submit" id="button-addon2">
                  <svg viewBox="0 0 1024 1024"><path d="M453.818182 23.272727C704.465455 23.272727 907.636364 226.443636 907.636364 477.090909c0 35.746909-4.142545 70.981818-12.264728 105.192727a46.545455 46.545455 0 0 1-90.577454-21.504c6.469818-27.182545 9.751273-55.202909 9.751273-83.688727C814.545455 277.876364 653.032727 116.363636 453.818182 116.363636 254.603636 116.363636 93.090909 277.876364 93.090909 477.090909 93.090909 676.305455 254.603636 837.818182 453.818182 837.818182c101.003636 0 195.211636-41.658182 262.981818-113.826909a46.545455 46.545455 0 0 1 63.650909-3.979637c2.978909 1.792 5.818182 3.956364 8.401455 6.446546l213.201454 205.684363a45.707636 45.707636 0 0 1 0.581818 65.233455l-0.581818 0.581818a46.545455 46.545455 0 0 1-65.233454 0.581818l-185.390546-178.827636A452.305455 452.305455 0 0 1 453.818182 930.909091C203.170909 930.909091 0 727.738182 0 477.090909S203.170909 23.272727 453.818182 23.272727z m76.613818 179.828364c86.714182 23.598545 147.2 76.078545 177.245091 154.973091a46.545455 46.545455 0 0 1-86.993455 33.140363c-19.176727-50.362182-55.994182-82.315636-114.688-98.280727a46.545455 46.545455 0 1 1 24.436364-89.832727z"  fill="#ffffff"></path></svg>
                  搜索
                  </button>
              </form>
            </div>

            {/* 轮播图内部 */}
            <div class="carousel-inner">
              <div class="carousel-item active">
                <img src={carouselFirstUrl} class="d-block w-100" alt="..." />
                <div class="carousel-caption d-none d-md-block">
                  {/* <h5>First slide label</h5> */}
                  <p>{carouselFirstCaption}</p>
                </div>
              </div>
              { carouselList.map((item) => (
                  <div class="carousel-item" index={item.id} >
                    <img src={item.url} class="d-block w-100" alt="..." />
                    <div class="carousel-caption d-none d-md-block">
                      <p>{item.caption}</p>
                    </div>
                  </div>
                  ))
              }
            </div>
          </div>

          {/* 中部TAB区域 */}
          <nav className='home-tab-container'>
            <div class="nav nav-tabs" id="nav-tab" role="tablist">
              <button class="nav-link active" id="nav-1-tab" data-bs-toggle="tab" data-bs-target="#nav-1" type="button" role="tab" aria-controls="nav-1" aria-selected="true">{tab.tab1.title}</button>
              <button class="nav-link" id="nav-2-tab" data-bs-toggle="tab" data-bs-target="#nav-2" type="button" role="tab" aria-controls="nav-2" aria-selected="false">{tab.tab2.title}</button>
              <button class="nav-link" id="nav-3-tab" data-bs-toggle="tab" data-bs-target="#nav-3" type="button" role="tab" aria-controls="nav-3" aria-selected="false">{tab.tab3.title}</button>
            </div>
          </nav>

          {/* 中部TAB内容显示区域 */}
          <div class="tab-content" id="nav-tabContent">
            <div class="tab-pane fade show active" id="nav-1" role="tabpanel" aria-labelledby="nav-1-tab">
              <div className='tab-description'>{tab.tab1.description}</div>
              <div className='tab-inner-container'>
                <div className='tab-inner-row first-tab-inner-row' >
                  <div className='tab-inner-row-title'>{tab.tab1.rows.rows1.title}</div>
                  {tab.tab1.rows.rows1.mytab.map(item=>(<MyTab {...item} />))}
                </div>
              </div>
            </div>
            <div class="tab-pane fade" id="nav-2" role="tabpanel" aria-labelledby="nav-2-tab">
              <div className='tab-description'>{tab.tab2.description}</div>
              <div className='tab-inner-container'>
                <div className='tab-inner-row' >
                  <div className='tab-inner-row-title'>{tab.tab2.rows.rows1.title}</div>
                  {tab.tab2.rows.rows1.mytab.map(item=>(<MyTab {...item} />))}
                </div>
                <div className='tab-inner-row' >
                  <div className='tab-inner-row-title'>{tab.tab2.rows.rows2.title}</div>
                  {tab.tab2.rows.rows2.mytab.map(item=>(<MyTab {...item} />))}
                </div>
              </div>
            </div>
            <div class="tab-pane fade" id="nav-3" role="tabpanel" aria-labelledby="nav-3-tab">
              <div className='tab-description'>{tab.tab3.description}</div>
              <div className='tab-inner-container'>
                <div className='tab-inner-row' >
                  <div className='tab-inner-row-title'>{tab.tab3.rows.rows1.title}</div>
                  {tab.tab3.rows.rows1.mytab.map(item=>(<MyTab {...item} />))}
                </div>
                <div className='tab-inner-row' >
                  <div className='tab-inner-row-title'>{tab.tab3.rows.rows2.title}</div>
                  {tab.tab3.rows.rows2.mytab.map(item=>(<MyTab {...item} />))}
                </div>
              </div>
            </div>
          </div>
        
      </div>
    )
  }
}

