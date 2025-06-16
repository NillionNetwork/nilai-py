from nilai_py import Client

client = Client(
    base_url="https://testnet-p0.nilai.sandbox.nilogy.xyz/nuc/v1/",
    nilauth_url="https://nilauth.sandbox.app-cluster.sandbox.nilogy.xyz",
    api_key="0680b9e64f23d180d08ac44784ab7ed665413d61076d4b3f6f7e41866dfda55c",
)
for i in range(10):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=[
            {"role": "user", "content": "Hello! Can you help me with something?"}
        ],
    )

    print(f"Response {i}: {response.choices[0].message.content}")
