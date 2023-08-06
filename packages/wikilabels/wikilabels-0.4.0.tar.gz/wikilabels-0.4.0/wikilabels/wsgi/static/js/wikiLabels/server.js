( function ($, WL) {

	var Server = function () {};
	Server.prototype.request = function (relPath, data, method) {
		var deferred = $.Deferred();
		method = method || "GET";
		$.ajax(
			this.absPath.apply(this, relPath),
			{
				dataType: "json",
				method: method,
				jsonp: false,
				crossDomain: true,
				xhrFields: {withCredentials: true},
				data: data || {}
			}
		)
			.done(function (doc, status, jqXHR) {
				if (!doc.error) {
					deferred.resolve(doc);
				} else {
					console.error(doc.error);
					deferred.reject(doc.error);
				}
			}.bind(this))
			.fail(function (jqXHR, status, err) {
				try {
					var errorMessage = $.parseJSON(jqXHR.responseText).error.message;
				}
				catch(parseError) {
					var errorMessage = "Unable to parse response";
				}
				var errorData = { code: jqXHR.status, status: status, message: errorMessage };
				console.error(errorData);
				deferred.reject(errorData);
			}.bind(this));

		return deferred.promise();
	};
	Server.prototype.absPath = function(/* relative path parts */){
		var serverRoot = WL.config.serverRoot,
		    relPath = WL.util.pathJoin.apply(this, Array.prototype.slice.call(arguments));

		return serverRoot.replace(/\/+$/g, "") + "/" + relPath.replace(/^\/+/g, "") + "/";
	};

	Server.prototype.getCampaigns = function () {
		return this.request(
			["campaigns", WL.mediawiki.dbname]
		);
	};
	Server.prototype.whoami = function () {
		return this.request(
			["auth", "whoami"]
		);
	};
	Server.prototype.getUserWorksetList = function (userId, campaignId) {
		return this.request(
			["users", userId, campaignId],
			{ worksets: "stats" }
		);
	};
	Server.prototype.assignWorkset = function (campaignId) {
		return this.request(
			["campaigns", WL.mediawiki.dbname, campaignId],
			{ workset: "stats"},
			"POST"
		);
	};
	Server.prototype.getWorkset = function (campaignId, worksetId) {
		return this.request(
			["campaigns", WL.mediawiki.dbname, campaignId, worksetId],
			{ tasks: "", campaign: "" }
		);
	};
	Server.prototype.getForm = function (formName) {
		return this.request(
			["forms", formName]
		);
	};
	Server.prototype.saveLabel = function (campaignId, worksetId, taskId, labelData) {
		return this.request(
			["campaigns", WL.mediawiki.dbname, campaignId, worksetId, taskId],
			{ label: JSON.stringify(labelData) },
			"POST"
		);
	};

	Server.prototype.abandonLabel = function (campaignId, worksetId, taskId) {
		return this.request(
			["campaigns", WL.mediawiki.dbname, campaignId, worksetId, taskId],
			{},
			"DELETE"
		);
	};
	WL.server = new Server();

})(jQuery, wikiLabels);
