import { render } from 'preact';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { App } from './app.jsx';
import './index.css';
import { store } from './redux/store';

render(
    <Provider store={store}>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </Provider>
    , document.getElementById('app')
    )
