var React = require('react');
import ReactDOM from 'react-dom';
(function(){
  var run = function(){
    ReactDOM.render(
      <h1>Hello, world!</h1>,
      document.getElementById('root')
    );
  }
  window.addEventListener('DOMContentLoaded', run, false);
})();
