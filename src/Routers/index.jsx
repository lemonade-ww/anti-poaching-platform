import React, { Component } from 'react'
import {Routes, Route, Navigate} from 'react-router-dom'
import {Home,Charts,Search,About} from '../Pages'

export default class Routers extends Component {
  render() {
    return (
        <Routes>
            <Route path='/' element={<Home/>}></Route>
            <Route path='/charts' element={<Charts/>}></Route>
            <Route path='/search' element={<Search/>}></Route>
            <Route path='/about' element={<About/>}></Route>
            <Route path="*" element={<Navigate to="/" />} />
        </Routes>
    )
  }
}
