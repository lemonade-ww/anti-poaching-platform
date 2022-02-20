// let results = require('../../../json/results2')
import results from '../../../json/results.json'
let originList = Object.values(results)


let refineFunc = (keyword)=>{
  // let keyword = 'education_level'
  let mymap = new Map()
  for (let item of originList) {
    if (item.defendant_info) {
      item.defendant_info.forEach((item)=>{
        let key = item[keyword] ? item[keyword] : '未知'
        if(mymap.has(key)){
          mymap.set(key, mymap.get(key)+1)
        } else {
          mymap.set(key, 1)
        }
      })
    }
  }

  let arr = []
  for (let [k,v] of mymap){
    let obj = {
      type: k,
      value: v
    }
    arr.push(obj)
  }

  return arr 
}

export default refineFunc