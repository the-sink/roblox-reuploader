local HttpService = game:GetService("HttpService")

local toolbar = plugin:CreateToolbar("Audio Reupload")
local captureButton = toolbar:CreateButton("Reupload", "Locates audio that will be unavailable after the permissions update, and attempts to re-upload them using an external server.", "rbxassetid://9087444202")

captureButton.ClickableWhenViewportHidden = true

local servicesToScan = {"Workspace", "Lighting", "ReplicatedFirst", "ReplicatedStorage", "ServerScriptService", "ServerStorage", "StarterGui", "StarterPack", "StarterPlayer", "SoundService", "Chat"}

local function httpRequest(url, data)
	return HttpService:RequestAsync({
		Url = url,
		Method = "POST",
		Headers = {["Content-Type"] = "application/json"},
		Body = data
	})
end

captureButton.Click:Connect(function()
	captureButton.Enabled = false
	
	local completed = false
	local audioIds = {}
	local replacements = {}
	
	local gui
	
	local success, err = pcall(function()
		print("Gathering asset IDs...")
		for _, serviceName in pairs(servicesToScan) do
			local service = game:GetService(serviceName)

			for _, object in pairs(service:GetDescendants()) do
				if object:IsA("Sound") and string.sub(object.SoundId, 1, 13) == "rbxassetid://" then
					local num = string.gsub(object.SoundId, "%D", "")
					local id = tonumber(num)

					if not table.find(audioIds, id) then
						table.insert(audioIds, id)
					end
				elseif object:IsA("Script") or object:IsA("LocalScript") or object:IsA("ModuleScript") then
					for id in string.gmatch(object.Source, "rbxassetid://%d+") do
						local num = string.gsub(id, "%D", "")
						id = tonumber(num)
						if not table.find(audioIds, id) then
							table.insert(audioIds, id)
						end
					end
				end
			end
		end
		
		-- Send audio IDs over to the server and wait for a response containing the list of IDs that need to be reuploaded
		
		if #audioIds > 0 then
			print("Found " .. #audioIds .. " asset IDs to send.")
			
			local data = HttpService:JSONEncode(audioIds)
		
			local response = httpRequest("http://localhost:37007/get-neccesary-downloads?creator_id=" .. tostring(game.CreatorId) .. "&creator_type=" .. tostring(game.CreatorType.Name) .. "&place_id=" .. tostring(game.PlaceId), data)
			
			local targetAudioAssets = HttpService:JSONDecode(response.Body)
			local amount = #targetAudioAssets
			

			if amount > 0 then
				print("Downloading and re-uploading required assets...")
				
				gui = script.Parent.ProgressGui:Clone()
				
				gui.Parent = game:GetService("CoreGui")
				
				local abort = false
				local continuing = false
				local elapsed = 0
				
				gui.Main.Confirmation.Label.Text = "Confirm re-upload of <b>" .. amount .. "</b> assets (at most):"
				
				gui.Main.Container.Abort.MouseButton1Down:Connect(function()
					abort = true
					gui.Main.Container.Abort.Visible = false
					gui.Main.Container.Label.Text = "<b>Aborting</b>"
				end)
				
				gui.Main.Confirmation.Yes.MouseButton1Down:Connect(function()
					continuing = true
					gui.Main.Container.Visible = true
					gui.Main.Confirmation.Visible = false
				end)
				
				gui.Main.Confirmation.No.MouseButton1Down:Connect(function()
					elapsed = 15
				end)
				
				repeat elapsed += task.wait() until continuing or elapsed >= 15
				
				if not continuing then
					print("Ignoring")
					gui:Destroy()
					return
				end
				
				for i, asset in pairs(targetAudioAssets) do
					if abort then break end
					pcall(function() -- Lazy fix, just in case someone messes with the gui
						if gui then
							local progress = i / amount
							
							gui.Main.Container.ProgressBar.Progress.Size = UDim2.new(progress, 0, 1, 0)
							gui.Main.Container.Label.Text = "Reupload in progress (<b>" .. math.round(progress*100) .. "%</b>)"
						end
					end)
					
					local assetUploadResponse = httpRequest("http://localhost:37007/reupload?asset_id=" .. asset.id .. "&file_name=" .. asset.name)
					
					if tonumber(assetUploadResponse.Body) then
						replacements[tostring(asset.id)] = assetUploadResponse.Body
					end
				end
				
				if not abort then
					print("Replacing audio IDs...")
					for _, serviceName in pairs(servicesToScan) do
						local service = game:GetService(serviceName)
					
						for _, object in pairs(service:GetDescendants()) do
							if object:IsA("Sound") and string.sub(object.SoundId, 1, 13) == "rbxassetid://" then
								local num = string.gsub(object.SoundId, "%D", "")
								
								if replacements[num] and tonumber(replacements[num]) > 0 then
									object.SoundId = "rbxassetid://" .. replacements[num]
								end
							elseif object:IsA("Script") or object:IsA("LocalScript") or object:IsA("ModuleScript") then
								local src = object.Source
								for id in string.gmatch(src, "rbxassetid://%d+") do
									id = string.gsub(id, "%D", "")
									
									if replacements[id] and tonumber(replacements[id]) > 0 then
										object.Source = string.gsub(object.Source, id, replacements[id])
									end
								end
							end
						end
					end
				else
					warn("Reupload has been aborted!")
				end
				
				completed = true
			else
				print("No audio assets have been determined by the Python server to need replacement. Check the built-in Audio Discovery plugin to make sure!")
			end
		else
			print("No asset IDs to send to the server!")
		end
	end)

	if success then
		print("Done")
	else
		warn("Error while capturing audio: " .. err .. "\nMake sure the Python server is running! If problems persist, submit an issue report or contact me on Discord at The_Sink#4096.")
	end
	
	if gui then
		gui:Destroy()
	end

	task.wait(3)

	captureButton.Enabled = true
end)