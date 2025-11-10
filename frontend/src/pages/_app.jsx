import { SessionProvider } from 'next-auth/react';
import Layout from '../components/layout/Layout';
import '../styles/globals.css';

const noLayoutRoutes = ['/login'];

function MyApp({ Component, pageProps: { session, ...pageProps }, router }) {
  const showLayout = !noLayoutRoutes.includes(router.pathname);

  return (
    <SessionProvider session={session}>
      {showLayout ? (
        <Layout>
          <Component {...pageProps} />
        </Layout>
      ) : (
        <Component {...pageProps} />
      )}
    </SessionProvider>
  );
}

export default MyApp;