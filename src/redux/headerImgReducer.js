export default function headerImgReducer(preState ,action){

  console.log(action)

  const {type} = action
  switch(type){
    case 'home':
      preState = {}
      break;
    case 'charts':
      preState = {backgroundImage: 'url(/img/bg5_1125_500.jpg)',backgroundPosition: 'bottom',}
      break;
    case 'search':
      preState = {backgroundImage:'url(/img/bg3_1125_500.jpg)',backgroundPosition:'middle',}
      break;
    case 'about':
      preState = {backgroundImage: 'url(/img/bg6_1125_500.jpg)',backgroundPosition: 'bottom',}
      break;
  }

  return {style:preState}

}