<script lang="ts">
	import Message from '../components/Message.svelte';
	import type { Chat, Video } from '../models';
	import { getTranscription, callGPT } from '$lib/requests';

	let chat: Chat = [
		{
			author: 'bot',
			content:
				"👋 I'm your YouTube Transcription Chatbot! Please share a YouTube video URL with me, and I'll extract the transcription to answer your questions based on the video's content. Just paste the URL, and let's get started!"
		}
	];

	let newMessage = '';
	let video: Video;
	const sendMessage = async () => {
		chat = [...chat, { author: 'user', content: newMessage }];
		if (!video) {
			let youtubeUrl = newMessage;
			newMessage = '';
			video = await getTranscription(youtubeUrl);
			chat = [
				...chat,
				{
					author: 'bot',
					content:
						"The transcription is complete. 🎉 Please feel free to ask me any questions you have about the video's content. Let's dive in!"
				}
			];
      return
		}

    const prompt = newMessage;
    newMessage = '';
		chat = [...chat, { author: 'bot', content: await callGPT(prompt, video) }];
	};
</script>

<div class=".container">
	<div class="row row-cols-1 row-cols-md-1 g-4">
		{#each chat as message}
			<Message {message} />{/each}
	</div>
	<div id="chat-form" style="margin-top: 10px;">
		<form method="POST" on:submit|preventDefault={sendMessage}>
			<div class="input-group mb-3">
				<input
					bind:value={newMessage}
					name="message"
					type="text"
					class="form-control"
					placeholder="Enter your message"
					aria-label="Enter your message"
					aria-describedby="button-addon2"
				/>
				<button class="btn btn-primary" type="submit" id="button-addon2"
					>Submit <i class="bi bi-send-fill"></i></button
				>
			</div>
		</form>
	</div>
</div>

<style>
	#chat-form {
		margin: auto;
		width: 60%;
	}
</style>
