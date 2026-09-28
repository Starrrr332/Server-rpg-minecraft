export async function onRequest(context) {
  const url = new URL(context.request.url);
  
  // Remove /map prefix to get original asset path
  let targetPath = url.pathname.replace(/^\/map/, '');
  if (!targetPath || targetPath === '') {
    targetPath = '/';
  }
  
  const targetUrl = `http://38.97.61.71:25898${targetPath}${url.search}`;

  const requestHeaders = new Headers(context.request.headers);
  requestHeaders.set('Host', 'ut09.holy.gg:25898');

  try {
    const response = await fetch(targetUrl, {
      method: context.request.method,
      headers: requestHeaders,
      body: ['GET', 'HEAD'].includes(context.request.method) ? undefined : context.request.body
    });

    const responseHeaders = new Headers(response.headers);
    // Allow embedding inside iframe and disable frame blocking
    responseHeaders.delete('X-Frame-Options');
    responseHeaders.delete('Content-Security-Policy');
    responseHeaders.set('Access-Control-Allow-Origin', '*');

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: responseHeaders
    });
  } catch (err) {
    return new Response(
      `<html><body style="background:#080c14;color:#fff;font-family:sans-serif;text-align:center;padding:50px;">` +
      `<h2>No se pudo conectar con el servidor BlueMap en el puerto 25898</h2>` +
      `<p style="color:#aaa;">${err.message}</p>` +
      `<p><a href="http://ut09.holy.gg:25898/" target="_blank" style="color:#38bdf8;">Abrir directamente vía HTTP</a></p>` +
      `</body></html>`,
      {
        status: 502,
        headers: { 'Content-Type': 'text/html; charset=utf-8' }
      }
    );
  }
}
