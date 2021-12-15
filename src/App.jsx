import React,{ Component } from "react"
import {Routes, Route, Navigate} from 'react-router-dom'

import {Header, Footer} from './Components'
import {Home,Charts,Search} from './Pages'

export default class App extends Component{
  state = {
    title:'中国野生动物大数据平台'
  }

  render(){
    return (
      <div>{this.state.title}
        <Header/>
        
          <Routes>
            <Route path='/home' element={<Home/>}></Route>
            <Route path='/charts' element={<Charts/>}></Route>
            <Route path='/search' element={<Search/>}></Route>
            <Route path="/home" render={() => <Navigate to="/home" />} />
          </Routes>

        <Footer/>
      </div>
    )
  }
}