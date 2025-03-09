import React from 'react';
import { Play, Pause, Settings2 } from 'lucide-react';
import { Track } from '../types/audio';

interface TrackCardProps {
  track: Track;
  trackState: {
    isPlaying: boolean;
    volume: number;
    playbackRate: number;
    pitch: number;
  };
  audioRef: (element: HTMLAudioElement | null) => void;
  onPlay: () => void;
  onPause: () => void;
  onVolumeChange: (volume: number) => void;
  onPlaybackRateChange: (rate: number) => void;
  onPitchChange: (pitch: number) => void;
  onPlayPause: () => void;
}

export const TrackCard: React.FC<TrackCardProps> = ({
  track,
  trackState,
  audioRef,
  onPlay,
  onPause,
  onVolumeChange,
  onPlaybackRateChange,
  onPitchChange,
}) => {
  const [showControls, setShowControls] = React.useState(true);
  const { volume, playbackRate, pitch } = trackState;

  return (
    <div className="p-4 space-y-4 bg-white rounded-lg shadow-sm">
      <audio ref={audioRef} src={track.url} loop />

      <div className="flex flex-col items-center space-y-2">
        <div className="flex justify-center items-center w-12 h-12 rounded-full">
          <img src={track.icon} alt="Track icon" className="w-14 h-14 text-white" />
        </div>
        <div className="text-center">
          <h3 className="font-medium text-gray-900">{track.title}</h3>
          {/* <p className="text-sm text-gray-500">{track.artist}</p> */}
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex justify-center space-x-2">
          <button
            onClick={trackState.isPlaying ? onPause : onPlay}
            className="p-2 text-white bg-blue-500 rounded-full transition-colors hover:bg-blue-600"
          >
            {trackState.isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
          </button>
          <button
            onClick={() => setShowControls(!showControls)}
            className={`p-2 rounded-full ${
              showControls ? 'text-white bg-blue-500' : 'text-gray-600 bg-gray-100'
            } hover:bg-blue-600 hover:text-white transition-colors`}
          >
            <Settings2 className="w-5 h-5" />
          </button>
        </div>

        {showControls && (
          <div className="space-y-2">
            <div>
              <label className="block text-xs font-medium text-gray-600">
                Volume: {(volume * 100).toFixed(0)}%
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={volume}
                onChange={e => onVolumeChange(parseFloat(e.target.value))}
                className="w-full h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600">
                Speed: {playbackRate.toFixed(1)}x
              </label>
              <input
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={playbackRate}
                onChange={e => onPlaybackRateChange(parseFloat(e.target.value))}
                className="w-full h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600">Pitch: {pitch}</label>
              <input
                type="range"
                min="-12"
                max="12"
                step="1"
                value={pitch}
                onChange={e => onPitchChange(parseFloat(e.target.value))}
                className="w-full h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
