import { FC, Fragment, PropsWithChildren } from 'react';
import './layout.css'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Layout: FC<PropsWithChildren> = ({ children }) => (
  <Fragment>
    <ToastContainer theme='dark'/>

    <div className='layout'>
      <div className='header'>
        <h2>Film review polarity</h2>
        <h3><a href="#">About project</a></h3>
      </div>

      <div className='main'>
        {children}
      </div>

      <div className='footer'>
        <a href='https://elmarsan.github.io/website/' target='_blank'>© 2023 Elías Martínez</a>
        <div className='footer-icons'>
          <a href='https://github.com/elmarsan' target='_blank' className='fa-brands fa-github'></a>
          <a href='https://linkedin.com/in/elias-martinez-74b07617a' className='fa-brands fa-linkedin'></a>
        </div>
      </div>
    </div>
  </Fragment>
);

export default Layout;