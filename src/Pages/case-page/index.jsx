import React from 'react'
import {useParams} from "react-router-dom";

export default function Case(){
  let { caseId } = useParams();

  const [caseInfo, setCaseInfo] = React.useState(
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

  return (
    <div className='common-container'> 

      <div className='related-search-container'>
        <div class="accordion" id="accordionPanelsStayOpenExample">  {/* 原始外层容器 */}
          {/* accordion 1 */}
          <div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-headingOne">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseOne" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                Accordion Item #1
              </button>
            </h2>
            <div id="panelsStayOpen-collapseOne" class="accordion-collapse collapse show" aria-labelledby="panelsStayOpen-headingOne">
              <div class="accordion-body">
                <strong>This is the first item's accordion body.</strong> It is shown by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
              </div>
            </div>
          </div>

          {/* accordion 2 */}
          <div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-headingTwo">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseTwo" aria-expanded="false" aria-controls="panelsStayOpen-collapseTwo">
                Accordion Item #2
              </button>
            </h2>
            <div id="panelsStayOpen-collapseTwo" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-headingTwo">
              <div class="accordion-body">
                <strong>This is the second item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
              </div>
            </div>
          </div>

          {/* accordion 3 */}
          <div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-headingThree">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseThree" aria-expanded="false" aria-controls="panelsStayOpen-collapseThree">
                Accordion Item #3
              </button>
            </h2>
            <div id="panelsStayOpen-collapseThree" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-headingThree">
              <div class="accordion-body">
                <strong>This is the third item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
              </div>
            </div>
          </div>

        </div>
      </div>

      <div className='case-container'>

        <table class="table table-hover">
          ...
        </table>
        
      </div>

    </div> 
  )
  
}
