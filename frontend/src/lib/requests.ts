// place files you want to import through the `$lib` alias in this folder.
import { env } from '$env/dynamic/public';
import type { Video } from '../models';

const getYoutubeId = (youtubeUrl: string): string => {
	const url = new URL(youtubeUrl);
	const youtubeId = url.searchParams.get('v');
	if (!youtubeId) {
		throw new Error(`Invalid youtube URL: ${youtubeUrl}`);
	}
	return youtubeId;
};
export const getTranscription = async (youtubeUrl: string): Promise<Video> => {
	const youtubeId = getYoutubeId(youtubeUrl);
	const response = await fetch(
		`${env.PUBLIC_BACKEND_URL}/api/v1/transcribe?youtube_id=${youtubeId}`
	);
	const result = await response.json();
	if (!response.ok) {
		throw new Error(result['detail']);
	}
	return result;
};

export const callGPT = async (prompt: string, video: Video): Promise<string> => {
	const data = {
		prompt: prompt,
		video: video
	};
	const response = await fetch(`${env.PUBLIC_BACKEND_URL}/api/v1/gpt`, {
		method: 'POST',
		body: JSON.stringify(data),
		headers: { 'Content-Type': 'application/json' }
	});
	const result = await response.json();
	if (!response.ok) {
		throw new Error(`😔 Sorry! There was an error calling GPT. ${result['detail']}`);
	}
	return result;
};
