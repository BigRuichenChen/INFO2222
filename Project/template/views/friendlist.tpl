<table class="styled">
    <thead>
        <tr>
            <th>Friend</th>
        </tr>
    </thead>
    <tbody>
            % for instance in friendlist:
                <!-- Each row is a link to each individual friend chat-->
                <tr>
                    <td><a href="/message/{{instance}}">{{instance}}</a></td>
                </tr>
            % end
    </tbody>
</table>