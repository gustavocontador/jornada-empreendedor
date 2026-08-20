import type { MetadataRoute } from "next";
import { getSiteUrl } from "@/lib/brand";

export default function robots(): MetadataRoute.Robots {
  const siteUrl = getSiteUrl();
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/checkout", "/carrinho", "/pedido/", "/api/"],
    },
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
