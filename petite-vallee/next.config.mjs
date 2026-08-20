/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // As imagens do catálogo vivem em /public. Quando as fotos oficiais
  // forem adicionadas, o componente next/image cuida da otimização.
  images: {
    formats: ["image/avif", "image/webp"],
  },
};

export default nextConfig;
