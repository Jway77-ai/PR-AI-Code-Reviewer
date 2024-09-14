//replace this with backend logic
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    const body = await request.json();
    const { message } = body;

    let botResponse = "I don't understand the question.";

    if (message.includes("diff")) {
        botResponse = "Here is a mock diff for your pull request.";
    } else if (message.includes("code quality")) {
        botResponse = "You could improve code quality by using more descriptive variable names.";
    }

    return NextResponse.json({ response: botResponse });
}
