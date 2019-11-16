(async () => {
	if (typeof(window) === 'undefined') {
		const
			fetch = require('nodejs-fetch'),
			fs = require('fs');
		if (!fs.existsSync('list.txt'))
			return console.error(new Error('list.txt not found'));
		let list = fs.readFileSync('list.txt', 'utf8').trim().split(',');
		let o = [
			"46/111/101/97/97/46/99/99", "99/99/111", "97/101/97", "111/101/97", "97/111/97", "99/101/101", "99/111/101", "111/99/97", "99/97/97",
			"101/97/101", "111/99/101", "101/97/111", "111/99/111", "101/111/111", "99/111/99", "97/99/111", "97/97/101", "99/111/111", "111/111/97",
			"99/97/111", "97/111/101", "111/101/111", "101/99/101", "101/101/111", "111/97/99", "101/101/99", "111/101/99", "101/111/101", "101/97/97",
			"101/111/97", "101/99/99", "99/101/99", "99/101/111", "97/101/101", "99/97/101", "101/111/99", "111/97/101", "99/99/101", "111/111/101",
			"97/97/111", "97/101/99", "99/99/97", "111/97/97"
		];
		let i = 0,
			h = t => t.split('/').map(v => String.fromCharCode(v)).join(''),
			s = h(o[0]);
		list.reduce((acc, n, i) => ((acc[i % 5] = acc[i % 5] || []).push(n), acc), []).forEach(async thread => {
			for (var id of thread) {
				await (new Promise((resolve, reject) => {
					fetch('https://a'+s+'/check.php?'+fetch.body({
						callback: 'jQuery0_0',
						v: id,
						f: 'mp3',
						k: 'DHwjDdFdbQdMvfbHbuDpQffvCC'
					}), {
						headers: { Referer: 'https://ytmp3.cc/' }
					}).then(d => d.text()).then(d => {
						let loop;
						d = JSON.parse(d.slice(10, -1));
						// console.log(d);
						d.title = d.title.replace(/\//g, '');
						if ((d.title.replace(/[^a-zа-я0-9]/gi, '').length ==  0) || fs.existsSync('files/'+d.title+'.mp3'))
							return resolve(console.log('Skip: '+d.title+' ('+Math.round(i / list.length * 100)+'%)'));
						console.log('Download: '+d.title+' ('+Math.round(i / list.length * 100)+'%)');
						(loop = () => fetch('https://a'+s+'/progress.php?'+fetch.body({
							callback: 'jQuery0_0',
							id: d.hash
						}), {
							headers: { Referer: 'https://ytmp3.cc/' }
						}).then(dd => dd.text()).then(dd => {
							dd = JSON.parse(dd.slice(10, -1));
							if (dd.progress != '3')
								setTimeout(() => loop(), 4000);
							else{
								fetch('https://'+h(o[dd.sid])+s+'/'+d.hash+'/'+id).then(res => {
									res.body.pipe(fs.createWriteStream('files/'+d.title+'.mp3')).on('finish', () => resolve());
								});
							}
						}))();
					});
				}));
				++i;
			}
		});
	}else
		document.body.append(Object.assign(document.createElement('script'), {
			src: 'https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9/crypto-js.js',
			onload: e => {
				e.target.remove();
				let time = Math.round(new Date().getTime()/1000),
					SAPISID = document.cookie.split('; ').map(v => v.split('=')).filter(v => (v[0] == 'SAPISID')).map(v => v[1]).join('');
				if (SAPISID)
					SAPISID = 'SAPISIDHASH '+time+'_'+CryptoJS.enc.Hex.stringify(CryptoJS.SHA1(time+' '+SAPISID+' '+location.origin));
				((res=[], loop) => (loop = (continuation, clickTrackingParams) => fetch('https://music.youtube.com/youtubei/v1/browse?'+(continuation ? 'ctoken='+continuation+'&continuation='+continuation+'&itct='+clickTrackingParams+'&' : '')+'alt=json&key='+ytcfg.data_.INNERTUBE_API_KEY, {
					method: "POST",
					credentials: 'include',
					headers: {
						'authorization': SAPISID,
						'content-type': 'application/json',
						'x-goog-visitor-id': ytcfg.data_.VISITOR_DATA,
						'x-youtube-client-name': ytcfg.data_.INNERTUBE_CONTEXT_CLIENT_NAME,
						'x-youtube-client-version': ytcfg.data_.INNERTUBE_CONTEXT_CLIENT_VERSION,
						'x-youtube-page-cl': ytcfg.data_.PAGE_CL,
						'x-youtube-page-label': ytcfg.data_.PAGE_BUILD_LABEL,
						'x-youtube-utc-offset': '300',
						'x-origin': 'https://music.youtube.com'
					},
					body: JSON.stringify({
						context: {
							client: {
								clientName: ytcfg.data_.INNERTUBE_CLIENT_NAME,
								clientVersion: ytcfg.data_.INNERTUBE_CONTEXT_CLIENT_VERSION,
								hl: ytcfg.data_.LOCALE.split('_')[0],
								gl: ytcfg.data_.LOCALE.split('_')[1],
								experimentIds: [],
								experimentsToken: '',
								utcOffsetMinutes: 300,
								locationInfo: { locationPermissionAuthorizationStatus: 'LOCATION_PERMISSION_AUTHORIZATION_STATUS_UNSUPPORTED' },
								musicAppInfo: {
									musicActivityMasterSwitch: 'MUSIC_ACTIVITY_MASTER_SWITCH_INDETERMINATE',
									musicLocationMasterSwitch: 'MUSIC_LOCATION_MASTER_SWITCH_INDETERMINATE',
									pwaInstallabilityStatus: 'PWA_INSTALLABILITY_STATUS_UNKNOWN'
								}
							},
							capabilities: {},
							request: {
								internalExperimentFlags: [{
									key: 'force_music_enable_outertube_playlist_detail_browse',
									value: 'true'
								}, {
									key: 'force_music_enable_outertube_tastebuilder_browse',
									value: 'true'
								}, {
									key: 'force_music_enable_outertube_search_suggestions',
									value: 'true'
								}],
								sessionIndex: {}
							},
							activePlayers: {},
							user: { enableSafetyMode: false }
						},
						browseId: JSON.parse(ytcfg.data_.INITIAL_ENDPOINT).browseEndpoint.browseId,
						browseEndpointContextSupportedConfigs: {
							browseEndpointContextMusicConfig: { pageType: 'MUSIC_PAGE_TYPE_PLAYLIST' }
						}
					})
				}).then(e => e.json()).then(e => {
					if (e.error)
						console.log(e.error);
					else{
						try {
							let obj = (
								e.continuationContents
								? e.continuationContents.musicPlaylistShelfContinuation
								: e.contents.singleColumnBrowseResultsRenderer.tabs[0].tabRenderer.content.sectionListRenderer.contents[0].musicPlaylistShelfRenderer
							);
							res = res.concat(obj.contents.map(v => v.musicResponsiveListItemRenderer.flexColumns[0].musicResponsiveListItemFlexColumnRenderer.text.runs[0].navigationEndpoint).filter(Boolean).map(v => v.watchEndpoint.videoId));
							if (obj.continuations)
								loop(obj.continuations[0].nextContinuationData.continuation, obj.continuations[0].nextContinuationData.clickTrackingParams);
							else
								Object.assign(document.createElement('a'), {
									href: URL.createObjectURL(new Blob([res.join()], {
										type: 'text/plain'
									})),
									download: 'list.txt'
								}).click();
						} catch (e) {
							return alert('Playlist not found');
						}
					}
				}))())();
			}
		}));
})();
