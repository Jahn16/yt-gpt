<script lang="ts">
	import Message from '../components/Message.svelte';
	import Export from '../components/Export.svelte';
	import Footer from '../components/Footer.svelte';
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
	let loading = false;
	let video: Video;
	const addMessageToChat = (message: string, author: string) => {
		chat = [...chat, { author, content: message }];
	};
	const sendMessage = async () => {
		loading = true;
		addMessageToChat(newMessage, 'user');
		if (!video) {
			let youtubeUrl = newMessage;
			newMessage = '';
			try {
				video = await getTranscription(youtubeUrl);
			} catch (e: unknown) {
				addMessageToChat(
					`😔 Sorry! There was an error fetching the transcription. ${e.message}`,
					'bot'
				);
				loading = false;
				return;
			}
			addMessageToChat(
				`📹 **Video:** ${video.title} <br /><br />
                 🎉 The transcription for the video is complete. <br />
                 🤔 Please feel free to ask me any questions you have about the video's content. Let's dive in!`,

				'bot'
			);
			loading = false;
			return;
		}

		const prompt = newMessage;
		newMessage = '';
		try {
			const gptResponse = await callGPT(prompt, video);
			addMessageToChat(gptResponse, 'bot');
		} catch (e: unknown) {
			addMessageToChat(e.message, 'bot');
		}
		loading = false;
	};
</script>

<div class="container w-100">
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
				<button class="btn btn-primary" type="submit" id="button-addon2" disabled={loading}>
					{#if loading}
						Loading
						<div class="spinner-border spinner-border-sm" role="status">
							<span class="sr-only"></span>
						</div>
					{:else}
						Submit <i class="bi bi-send-fill"></i>
					{/if}
				</button>
			</div>
		</form>
		<Export {chat} />
	</div>

	<Footer />
</div>

<style>
	#chat-form {
		margin: auto;
		width: 60%;
	}
</style>
