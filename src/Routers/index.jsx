import React, { Component } from 'react'
import {Routes, Route, Navigate} from 'react-router-dom'
import {Home,Charts,Search,About,Case,Advance,Result, ChartsNav, Statistics, Map,
        Aboutus, Contact} from '../Pages'

export default class Routers extends Component {
  render() {
    return (
        <Routes>
            <Route path='/' element={<Home/>}></Route>
            <Route path='/charts' element={<Charts/>}>
              <Route index element={<ChartsNav/>}/>
              <Route path="/charts/statistics" element={<Statistics/>}/>
              <Route path="/charts/map" element={<Map/>}/>
            </Route>
            <Route path='/search' element={<Search/>}>
              <Route index element={<Advance/>}/>
              <Route path="/search/result" element={<Result/>}/>
              <Route path="/search/case_:caseId" element={<Case/>} />
            </Route>
            <Route path='/about' element={<About/>}>
              <Route index element={<Aboutus/>}/>
              <Route path='/about/contact' element={<Contact/>}/>
            </Route>
            <Route path="*" element={<Navigate to="/" />} />
        </Routes>
    )
  }
}
