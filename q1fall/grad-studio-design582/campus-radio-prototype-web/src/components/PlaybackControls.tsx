import React from 'react';

interface PlaybackControlsProps {
  playbackRate: number;
  pitch: number;
  onPlaybackRateChange: (rate: number) => void;
  onPitchChange: (pitch: number) => void;
}

export const PlaybackControls: React.FC<PlaybackControlsProps> = ({
  playbackRate,
  pitch,
  onPlaybackRateChange,
  onPitchChange
}) => {
  return (
    <div className="flex flex-col space-y-4 w-full max-w-md">
      <div>
        <label className="block mb-1 text-sm font-medium text-gray-700">
          Playback Speed: {playbackRate.toFixed(1)}x
        </label>
        <input
          type="range"
          min="0.5"
          max="2"
          step="0.1"
          value={playbackRate}
          onChange={(e) => onPlaybackRateChange(parseFloat(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
      </div>
      <div>
        <label className="block mb-1 text-sm font-medium text-gray-700">
          Pitch Adjustment: {pitch.toFixed(1)}
        </label>
        <input
          type="range"
          min="-12"
          max="12"
          step="1"
          value={pitch}
          onChange={(e) => onPitchChange(parseFloat(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
      </div>
    </div>
  );
};