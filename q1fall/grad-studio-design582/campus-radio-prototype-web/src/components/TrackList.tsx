import React from 'react';
import { Track } from '../types/audio';
import { TrackCard } from './TrackCard';

interface TrackListProps {
  tracks: Track[];
  getTrackState: (trackId: number) => {
    isPlaying: boolean;
    volume: number;
    playbackRate: number;
    pitch: number;
  };
  audioRefs: React.MutableRefObject<Map<number, HTMLAudioElement>>;
  onPlay: (trackId: number) => void;
  onPause: (trackId: number) => void;
  onVolumeChange: (trackId: number, volume: number) => void;
  onPlaybackRateChange: (trackId: number, rate: number) => void;
  onPitchChange: (trackId: number, pitch: number) => void;
}

export const TrackList: React.FC<TrackListProps> = ({
  tracks,
  getTrackState,
  audioRefs,
  onPlay,
  onPause,
  onVolumeChange,
  onPlaybackRateChange,
  onPitchChange,
}) => {
  return (
    <div className="grid grid-cols-3 gap-4">
      {tracks.map(track => (
        <TrackCard
          key={track.id}
          track={track}
          trackState={getTrackState(track.id)}
          audioRef={element => {
            if (element) {
              audioRefs.current.set(track.id, element);
            }
          }}
          onPlay={() => onPlay(track.id)}
          onPause={() => onPause(track.id)}
          onVolumeChange={volume => onVolumeChange(track.id, volume)}
          onPlaybackRateChange={rate => onPlaybackRateChange(track.id, rate)}
          onPitchChange={pitch => onPitchChange(track.id, pitch)}
          onPlayPause={() =>
            getTrackState(track.id).isPlaying ? onPause(track.id) : onPlay(track.id)
          }
        />
      ))}
    </div>
  );
};
