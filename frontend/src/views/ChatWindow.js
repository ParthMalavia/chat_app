import React from 'react';
import {
	Box,
	Divider,
	Avatar,
	Typography,
	Paper,
	TextField,
	Button,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';


export default function ChatWindow({ recipient, messages, user_id, newMessage, setNewMessage, sendMessage }) {

	function handleSubmit(event) {
		event.preventDefault()
		sendMessage()
	}
	function handleChange(event) {
		setNewMessage(event.target.value)
	}

	return (
		<Paper elevation={3} sx={{ p: 2 }}>
			<Box sx={{ display: 'flex', alignItems: 'center' }}>
				<Avatar src={recipient.image} />
				<Typography variant="h6" sx={{ ml: 1 }}>{recipient.full_name}</Typography>
			</Box>
			<Divider sx={{ my: 2 }} />
			<Box sx={{ padding: 2, height: "400px", overflowY: 'auto', position: 'relative', display: 'flex', flexDirection: "column" }}>
				{messages.map((message) => (
					<div key={message.id}>
						<Box
							sx={{
								borderRadius: '10px',
								padding: '10px',
								mb: 2,
								...(message.sender === user_id ? { backgroundColor: '#e0f2f1', float: 'right' } : { backgroundColor: '#fafafa', float: 'left' }),
							}}
						>
							<Typography>{message.message}</Typography>
						</Box>
					</div>
				))}

			</Box>
			<Box component="form" onSubmit={handleSubmit} sx={{ position: 'fix', bottom: 0, width: '100%', p: 1, display: 'flex' }}>
				<TextField
					variant="outlined"
					placeholder="Type your message"
					fullWidth
					value={newMessage}
					onChange={handleChange}
				/>
				<Button type='submit' onClick={sendMessage} ><SendIcon /></Button>
			</Box>
		</Paper>
	);
};
