import { FC, PropsWithChildren } from 'react';
import './layout.css'

const Layout: FC<PropsWithChildren> = ({ children }) => (
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
);

export default Layout;