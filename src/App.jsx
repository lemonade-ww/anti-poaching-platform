import React,{ Component } from "react"

export default class App extends Component{
  state = {
    title:'中国野生动物大数据平台'
  }

  render(){
    return (
      <div>{this.state.title}</div>
    )
  }
}

