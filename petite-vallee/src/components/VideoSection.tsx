"use client";

import { useState } from "react";
import { BotanicalDecoration } from "./BotanicalDecoration";

/**
 * Seção do vídeo institucional.
 *
 * O vídeo ainda não foi fornecido. Quando chegar, configure UMA
 * das opções abaixo:
 *   - `fileSrc`: caminho de um arquivo enviado para /public
 *     (ex.: "/videos/nossa-historia.mp4"), ou
 *   - `embedUrl`: URL de incorporação do YouTube/Vimeo
 *     (ex.: "https://www.youtube-nocookie.com/embed/XXXX").
 *
 * Regras: sem autoplay com som; thumbnail elegante com botão de
 * play; proporção 16:9 responsiva; placeholder claro enquanto o
 * vídeo não existe.
 */

interface VideoSectionProps {
  fileSrc?: string;
  embedUrl?: string;
  posterSrc?: string;
  title?: string;
}

export function VideoSection({
  fileSrc,
  embedUrl,
  posterSrc,
  title = "A história da Petite Vallée",
}: VideoSectionProps) {
  const [activated, setActivated] = useState(false);
  const hasVideo = Boolean(fileSrc || embedUrl);

  if (!hasVideo) {
    return (
      <div className="video-frame video-frame--placeholder" role="img" aria-label="Espaço reservado para o vídeo institucional, em breve">
        <BotanicalDecoration size={34} />
        <p className="video-frame__placeholder-title">{title}</p>
        <p className="video-frame__placeholder-note">
          Nosso vídeo está sendo preparado e aparecerá aqui em breve.
        </p>
      </div>
    );
  }

  if (!activated) {
    return (
      <div className="video-frame">
        {posterSrc && (
          /* eslint-disable-next-line @next/next/no-img-element */
          <img src={posterSrc} alt="" className="video-frame__poster" />
        )}
        <button
          type="button"
          className="video-frame__play"
          onClick={() => setActivated(true)}
          aria-label={`Assistir: ${title}`}
        >
          <span className="video-frame__play-circle" aria-hidden="true">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5.5v13l11-6.5-11-6.5z" />
            </svg>
          </span>
          <span className="video-frame__play-label">Assistir ao vídeo</span>
        </button>
      </div>
    );
  }

  if (fileSrc) {
    return (
      <div className="video-frame">
        {/* controles nativos acessíveis; sem autoplay com som */}
        <video controls autoPlay muted={false} preload="metadata" poster={posterSrc}>
          <source src={fileSrc} />
          Seu navegador não suporta a reprodução deste vídeo.
        </video>
      </div>
    );
  }

  return (
    <div className="video-frame">
      <iframe
        src={embedUrl}
        title={title}
        allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        loading="lazy"
      />
    </div>
  );
}
