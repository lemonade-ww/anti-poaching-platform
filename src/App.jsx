import React,{ Component } from "react"
import {Header, Footer} from './Components'
import Routers from './Routers'

export default class App extends Component{
  state = {
    title:'中国野生动物大数据平台'
  }

  render(){
    return (
      <div>
        <Header/>
        <Routers/>
        <Footer/>
      </div>
    )
  }
}